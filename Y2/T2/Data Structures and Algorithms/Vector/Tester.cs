using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace SortingOrder
{
    class Tester
    {
        static void Main(string[] args)
        {
            List<int> correct = new List<int>(TestGenerator.Count());
            List<int> incorrect = new List<int>(TestGenerator.Count());
            int scores = 0;

            for (int i = 0; i < TestGenerator.Count(); i++)
            {
                try
                {

                    SortingOrder order = new SortingOrder();
                    string[] a1; int[] a2; int[] a3;
                    string result = TestGenerator.Generate(i, out a1, out a2, out a3);
                    Console.WriteLine("\nAttempting test instance {0} of the following structure:\n  names:\t[{1}]\n  ages:  \t[{2}]\n  weights\t[{3}]\nThe expected answer is {4}.", 
                        i, String.Join(",",a1), String.Join(",", a2), String.Join(",", a3), result);
                    Stopwatch watch = new Stopwatch();
                    watch.Start();
                    string answer = SortingOrder.Solve(a1, a2, a3);
                    if (result == answer)
                    {
                        scores++;
                        correct.Add(i);
                        Console.WriteLine(" :: SUCCESS (Time elapsed {0})", watch.Elapsed);
                    }
                    else
                    {
                        incorrect.Add(i);
                        Console.WriteLine(" :: FAILED with an incorrect answer of {0}", answer);
                    }
                }
                catch (Exception e)
                {
                    incorrect.Add(i);
                    Console.WriteLine(" :: FAILED with the runtime error {1}", i, e.ToString());
                }
            }

            Console.WriteLine("\nSummary: {0} tests out of {1} passed", scores, TestGenerator.Count());
            Console.WriteLine("Tests passed ({1} to {2}): {0}", correct.Count == 0 ? "none" : string.Join(", ", correct), 0, TestGenerator.Count());
            Console.WriteLine("Tests failed ({1} to {2}): {0}", incorrect.Count == 0 ? "none" : string.Join(", ", incorrect), 0, TestGenerator.Count());

            Console.ReadKey();
        }

    }
}