package com.trojan.ai;

import java.util.ArrayList;
import java.util.List;

/**
 * Planner
 * -------
 * Converts a high-level user prompt into an ordered list of tool-ready steps.
 * This example uses keyword heuristics; you can later swap in an LLM call.
 *
 * Compile:
 *   mvn package   (produces target/planner.jar)
 *
 * Usage from Python (JPype):
 *   JavaPlanner planner = jpype.JClass("com.trojan.ai.Planner")();
 *   List<String> steps  = planner.createPlan("Compare vectors ...");
 */
public class Planner {

    /** Split prompt into lower-case tokens for quick heuristics. */
    private String[] tokenize(String prompt) {
        return prompt.toLowerCase().split("\\s+");
    }

    /**
     * Create an ordered execution plan.
     * @param prompt  Raw user request
     * @return        List of step strings
     */
    public List<String> createPlan(String prompt) {
        List<String> steps = new ArrayList<>();
        String[] tokens   = tokenize(prompt);

        // Heuristic 1: vector comparison
        for (String t : tokens) {
            if (t.contains("vector")) {
                steps.add("vector_similarity");
                break;
            }
        }

        // Heuristic 2: web search
        for (String t : tokens) {
            if (t.contains("search") || t.contains("web")) {
                steps.add("web_search");
                break;
            }
        }

        // Default: ask LLM to draft summary
        steps.add("llm_summary");

        return steps;
    }
}
