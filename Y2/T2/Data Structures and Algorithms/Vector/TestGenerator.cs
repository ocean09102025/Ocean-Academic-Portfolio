using System;

namespace SortingOrder
{
    class TestGenerator
    {
        static public int Count()
        {
            return 12;
        }

        public static string Generate(int k, out string[] a1, out int[] a2, out int[] a3)
        {
            string result = "";
            a1 = null; a2 = null; a3 = null;
            switch (k)
            {
                case 0: a1 = new string[] { "BOB", "BOB", "DAVE", "JOE" }; a2 = new int[] { 22, 35, 35, 30 }; a3 = new int[] { 122, 122, 195, 200 }; result = "IND"; break;
                case 1: a1 = new string[] { "BOB", "BOB", "DAVE", "DAVE" }; a2 = new int[] { 22, 35, 35, 30 }; a3 = new int[] { 122, 122, 195, 200 }; result = "NOT"; break;
                case 2: a1 = new string[] { "BOB", "BOB", "DAVE", "DAVE" }; a2 = new int[] { 22, 35, 35, 30 }; a3 = new int[] { 122, 122, 195, 190 }; result = "NWA"; break;
                case 3: a1 = new string[] { "A", "A", "A", "AA", "A" }; a2 = new int[] { 3, 8, 2, 4, 9 }; a3 = new int[] { 175, 173, 160, 160, 122 }; result = "IND"; break;
                case 4: a1 = new string[] { "A", "A", "AAA", "AA", "A" }; a2 = new int[] { 3, 8, 2, 4, 9 }; a3 = new int[] { 175, 173, 160, 160, 122 }; result = "WAN"; break;
                case 5: a1 = new string[] { "A", "A", "A", "B", "B", "C" }; a2 = new int[] { 48, 48, 72, 70, 71, 75 }; a3 = new int[] { 10, 10, 9, 9, 8, 8 }; result = "IND"; break;
                case 6: a1 = new string[] { "A", "B", "A", "B", "B", "C" }; a2 = new int[] { 48, 48, 72, 70, 71, 75 }; a3 = new int[] { 10, 10, 9, 9, 8, 8 }; result = "WNA"; break;
                case 7: a1 = new string[] { "D", "D", "D", "D", "D", "D" }; a2 = new int[] { 1, 2, 3, 4, 5, 6 }; a3 = new int[] { 6, 5, 4, 1, 3, 2 }; result = "IND"; break;
                case 8: a1 = new string[] { "JEREMIAH", "BOB", "BOB" }; a2 = new int[] { 7, 2, 3 }; a3 = new int[] { 200, 180, 180 }; result = "IND"; break;
                case 9: a1 = new string[] { "JEREMIAH", "JEREMIAH", "YAHOUDI" }; a2 = new int[] { 7, 12, 3 }; a3 = new int[] { 200, 220, 220 }; result = "NAW"; break;
                case 10: a1 = new string[] { "A", "B", "C", "C", "A", "A", "A" }; a2 = new int[] { 1, 1, 1, 1, 2, 2, 2 }; a3 = new int[] { 200, 230, 240, 230, 300, 300, 198 }; result = "ANW"; break;
                case 11: a1 = new string[] { "DAVE", "EDGAR", "AL", "AL", "BILL", "BILL", "ABLE", "AL", "JIM", "JIM" }; a2 = new int[] { 20, 21, 22, 23, 23, 23, 23, 24, 25, 25 }; a3 = new int[] { 150, 180, 200, 212, 212, 200, 100, 223, 229, 229 }; result = "AWN"; break;
                case 12: a1 = new string[] { "DAVE", "EDGAR", "ALL", "AL", "BILL", "BILL", "ABLE", "AL", "JIM", "JIM" }; a2 = new int[] { 20, 21, 22, 23, 23, 23, 23, 25, 25, 25 }; a3 = new int[] { 150, 180, 200, 212, 212, 200, 100, 223, 229, 229 }; result = "NOT"; break;
                case 13: a1 = new string[] { "DAVE", "EDGAR", "AL", "AL", "AL", "AL", "ABLE", "AL", "JIM", "JIM" }; a2 = new int[] { 20, 21, 22, 23, 23, 23, 23, 24, 25, 25 }; a3 = new int[] { 150, 180, 212, 212, 212, 212, 201, 223, 229, 229 }; result = "AWN"; break;
                case 14: a1 = new string[] { "A", "B", "C", "C", "A", "A", "A" }; a2 = new int[] { 1, 1, 1, 1, 2, 2, 2 }; a3 = new int[] { 260, 250, 240, 240, 300, 300, 198 }; result = "IND"; break;
                case 15: a1 = new string[] { "A", "B", "C", "C", "A", "A", "A" }; a2 = new int[] { 1, 1, 1, 1, 1, 1, 1 }; a3 = new int[] { 200, 230, 240, 230, 300, 300, 198 }; result = "NOT"; break;
                case 16: a1 = new string[] { "JEREMIAHJONES", "JEREMIAH", "YAHOUDI" }; a2 = new int[] { 7, 12, 3 }; a3 = new int[] { 200, 220, 220 }; result = "NOT"; break;
                case 17: a1 = new string[] { "JEREMIAH", "JEREMIAH", "YAHOUDI" }; a2 = new int[] { 7, 12, 3 }; a3 = new int[] { 220, 220, 220 }; result = "IND"; break;
                case 18: a1 = new string[] { "A", "B", "A", "A", "B", "C" }; a2 = new int[] { 48, 48, 72, 70, 71, 75 }; a3 = new int[] { 10, 10, 9, 9, 8, 8 }; result = "NOT"; break;
                case 19: a1 = new string[] { "A", "B", "A", "B", "B", "C", "C" }; a2 = new int[] { 48, 48, 72, 70, 71, 75, 75 }; a3 = new int[] { 10, 10, 9, 9, 8, 8, 8 }; result = "WNA"; break;
                case 20: a1 = new string[] { "BOB", "BOB", "DAVE", "DAVE" }; a2 = new int[] { 22, 35, 35, 30 }; a3 = new int[] { 122, 122, 195, 200 }; result = "NOT"; break;
                case 21: a1 = new string[] { "BOB", "BOB", "DAVE", "JOE" }; a2 = new int[] { 22, 35, 35, 30 }; a3 = new int[] { 122, 122, 195, 200 }; result = "IND"; break;
                case 22: a1 = new string[] { "BOB", "BOB", "DAVE", "DAVE" }; a2 = new int[] { 22, 35, 35, 30 }; a3 = new int[] { 122, 122, 195, 190 }; result = "NWA"; break;
                case 23: a1 = new string[] { "DAVE", "DAVE", "BOB", "DAVE" }; a2 = new int[] { 25, 30, 30, 25 }; a3 = new int[] { 200, 200, 180, 180 }; result = "WNA"; break;
                case 24: a1 = new string[] { "BOB", "BOB" }; a2 = new int[] { 20, 20 }; a3 = new int[] { 100, 100 }; result = "IND"; break;
                case 25: a1 = new string[] { "ZZZ", "AAA", "AAA" }; a2 = new int[] { 1, 2, 3 }; a3 = new int[] { 66, 55, 44 }; result = "IND"; break;
                case 26: a1 = new string[] { "BOB", "BOB" }; a2 = new int[] { 200, 40 }; a3 = new int[] { 2, 2 }; result = "NOT"; break;
                case 27: a1 = new string[] { "A", "B", "D", "D" }; a2 = new int[] { 3, 2, 3, 4 }; a3 = new int[] { 1, 1, 1, 2 }; result = "NAW"; break;
            }
            return result;

        }
    }
}