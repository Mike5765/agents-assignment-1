"""
Task Definitions for Research Crew

TODO: Define the four sequential tasks:
1. Query Expansion - Break down the research question
2. Source Hunting - Search the paper corpus
3. Synthesis - Analyze and synthesize findings
4. Report Writing - Generate the literature review

Each task should:
- Have a clear description telling the agent what to do
- Specify the agent responsible
- Define expected_output format
- Use context parameter to pass information between tasks
"""

from crewai import Task
from agents import query_expander, source_hunter, synthesizer, report_writer


def create_research_tasks(research_question: str) -> list[Task]:
    """
    Create the task pipeline for a research question.

    Args:
        research_question: The user's research question

    Returns:
        List of 4 tasks in execution order

    TODO: Implement the four tasks below
    """

    # =========================================
    # Task 1: Query Expansion
    # =========================================
    # TODO: Create a task that breaks down the research question
    # into sub-questions, keywords, and search angles
    
    expand_task = Task(
        description=f"Take the following research question and break it down into a comprehensive " \
        f"search strategy:\n\n'{research_question}'\n\n" \
        f"Generate 6-8 focused sub-questions that approach the topic from completely different angles: " \
        f"(1) theoretical foundations, (2) practical implementations, (3) performance and benchmarks, " \
        f"(4) limitations and critiques, (5) comparisons with alternative approaches, " \
        f"(6) applications in multi-agent systems, (7) historical development, (8) future directions. " \
        f"For each sub-question, provide 4-6 unique keywords not used in any other sub-question. " \
        f"The goal is for each sub-question to surface a completely different paper from the corpus. "
        f"The corpus contains these papers: Wooldridge 1995, Wang 2023 survey, Xi 2023 survey, " \
        f"ReAct, Chain-of-Thought, Tree of Thoughts, Reflexion, CAMEL, Generative Agents, AutoGen, " \
        f"Toolformer, RAG 2020, RAG Survey 2023, Planning Abilities, Constitutional AI. " \
        f"For each sub-question, explicitly name which corpus papers are most likely relevant.",

        agent=query_expander,
        
        expected_output="A structured markdown document containing:\n" \
        "1. A restatement of the original research question\n" \
        "2. 6-8 sub-questions each targeting a different angle with unique keywords\n" \
        "3. A list of specific papers from the corpus that should be searched for each sub-question\n" \
        "4. Explicit instructions to the source hunter to avoid repeating the same paper twice"
    )

    # =========================================
    # Task 2: Source Hunting
    # =========================================
    # TODO: Create a task that searches the paper corpus
    # Hint: Use context=[expand_task] to pass the query strategy
    
    search_task = Task(
        description="Using the query strategy from the previous task, search the research " \
        "paper corpus for relevant passages. You must call the search_papers tool at least " \
        "8 times using different search queries. For each paper named in the query strategy, " \
        "run at least one dedicated search. Collect 12-15 of the most relevant passages " \
        "spread across at least 6 different papers. For every passage you retrieve, record " \
        "the exact paper title, authors, and year as returned by the search tool. " \
        "Do not invent or guess any citation details, only use what the search tool returns. " \
        "If a search returns no results, try different keywords before moving on.",
        
        agent=source_hunter,
        context=[expand_task],

        expected_output="A structured list of 12-15 retrieved passages, each including:\n" \
        "- Exact paper title, authors, and year as returned by the search tool\n" \
        "- The relevant passage or summary\n" \
        "- Why this passage is relevant to the research question\n" \
        "- A note confirming this came from the search tool, not from memory"
    )

    # =========================================
    # Task 3: Synthesis
    # =========================================
    # TODO: Create a task that synthesizes findings into themes
    # Hint: Use context=[expand_task, search_task] for full context
    
    synthesis_task = Task(
        description="Analyze only the passages retrieved in the previous task and synthesize " \
        "the findings. Do not introduce any papers, authors, or findings that were not " \
        "explicitly provided in the source hunter results. Identify 3-5 major themes that " \
        "emerge across the retrieved passages. For each theme you must: " \
        "(1) identify which specific papers contribute to it and how they differ in approach, " \
        "(2) find at least one direct tension or contradiction between two specific papers and " \
        "explain what it reveals about the state of the field, " \
        "(3) go beyond summarizing what papers say by analyzing why they disagree or agree " \
        "and what implications that has for the research area, " \
        "(4) identify a specific unanswered question that the tension between papers raises. " \
        "A theme that simply lists what papers say without analyzing their relationships " \
        "is not acceptable. Every theme must show critical thinking, not summarization.",

        agent=synthesizer,
        context=[expand_task, search_task],

        expected_output="A synthesis document containing:\n" \
        "1. 3-5 themes each with named paper-to-paper tensions and contradictions\n" \
        "2. For each theme, an analysis of WHY papers agree or disagree\n" \
        "3. Specific unanswered questions raised by each tension\n" \
        "4. Identified gaps in the existing literature\n" \
        "5. A note that no sources were introduced beyond what the search tool returned"
    )

    # =========================================
    # Task 4: Report Writing
    # =========================================
    # TODO: Create a task that writes the final literature review
    # Hint: Use context=[expand_task, search_task, synthesis_task]
    
    report_task = Task(
        description="Using all prior research, the query strategy, retrieved passages, and " \
        "synthesis, write a complete, polished literature review in markdown format. " \
        "Only cite papers that appear in the source hunter results and synthesis. " \
        "Never introduce new authors or papers not found in the previous tasks. " \
        "If a theme lacks a verified citation, note that further research is needed " \
        "rather than inventing a source. Use in-text citations in (Author, Year) format " \
        "throughout, and include a full references list at the end.",

        agent=report_writer,
        context=[expand_task, search_task, synthesis_task],

        expected_output="A complete literature review in markdown with these sections:\n" \
        "# Literature Review: [Research Question]\n" \
        "## Executive Summary\n" \
        "## Introduction\n" \
        "## Methodology\n" \
        "## Findings\n" \
        "### Theme 1: ...\n" \
        "### Theme 2: ...\n" \
        "### Theme 3: ...\n" \
        "## Discussion\n" \
        "## Conclusion\n" \
        "## References"
    )

    # TODO: Return your tasks in order
    return [expand_task, search_task, synthesis_task, report_task]


