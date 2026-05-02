package com.trojan.ai;

import java.util.ArrayList;
import java.util.List;

/**
 * High-level task planner for HelixAgent.
 * Converts user prompts into ordered sequences of steps.
 */
public class Planner {
    
    /**
     * Create an execution plan from a natural language prompt.
     * 
     * @param prompt User's high-level request
     * @return Ordered list of action steps (e.g., ["web_search", "llm_summary"])
     */
    public List<String> createPlan(String prompt) {
        List<String> steps = new ArrayList<>();
        String lower = prompt.toLowerCase();
        
        // Simple keyword-based planning (can be replaced with LLM later)
        if (lower.contains("vector") || lower.contains("similarity")) {
            steps.add("vector_similarity");
        }
        
        if (lower.contains("search") || lower.contains("web")) {
            steps.add("web_search");
        }
        
        if (lower.contains("summarize") || lower.contains("summary")) {
            steps.add("llm_summary");
        }
        
        // Always add a reasoning step at the end
        if (steps.isEmpty()) {
            steps.add("llm_reasoning");
        }
        
        return steps;
    }
}