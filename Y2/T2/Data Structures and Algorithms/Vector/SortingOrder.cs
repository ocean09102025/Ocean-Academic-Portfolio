using System;
using System.Collections.Generic;

namespace SortingOrder
{
    public class SortingOrder
    {
        // Main method that determines the sorting rule used
        public static string Solve(string[] name, int[] age, int[] weight)
        {
            int n = name.Length; // Get number of elements in the arrays

            // List of all 6 valid sorting rules: primary → secondary → tertiary
            string[] rules = { "NAW", "NWA", "ANW", "AWN", "WAN", "WNA" };

            // Store rules that correctly match the order of the input arrays
            List<string> matches = new List<string>();

            // Try each sorting rule
            for (int r = 0; r < rules.Length; r++)
            {
                bool ok = true; // Assume the rule is valid until proven otherwise

                // Compare each pair of adjacent items in the arrays
                for (int i = 0; i < n - 1; i++)
                {
                    // Compare item i and i+1 using the current rule
                    int cmp = Compare(rules[r], name[i], age[i], weight[i], name[i + 1], age[i + 1], weight[i + 1]);

                    // If item[i] should not come before item[i+1], rule is invalid
                    if (cmp > 0)
                    {
                        ok = false; // Rule is invalid for this test
                        break; // Stop checking this rule
                    }
                }

                // If all items are in correct order for this rule, add it to matches
                if (ok) matches.Add(rules[r]);
            }

            // Decide final result based on how many rules matched

            if (matches.Count == 0) return "NOT";     // No rule matches
            if (matches.Count == 1) return matches[0]; // Exactly one rule matches
            return "IND"; // Multiple rules matched (indeterminate)
        }

        // Helper function: compares two items based on a rule (e.g., "NAW")
        private static int Compare(string rule, string n1, int a1, int w1, string n2, int a2, int w2)
        {
            // Go through each character in the rule (3 levels of keys)
            for (int i = 0; i < 3; i++)
            {
                char key = rule[i]; // Get current key character (N, A, or W)
                int cmp = 0;

                // Compare based on the current key:
                if (key == 'N') cmp = n1.CompareTo(n2); // Name: alphabetical (A → Z)
                else if (key == 'A') cmp = a1.CompareTo(a2); // Age: ascending
                else if (key == 'W') cmp = -w1.CompareTo(w2); // Weight: descending, so we reverse it

                // If the two items are different, return the comparison result
                if (cmp != 0)
                    return cmp;
                // If they are equal, move to the next key (tie-breaker)
            }

            // If all keys are equal (no differences), return 0
            return 0;
        }
    }
}
