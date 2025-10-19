using Microsoft.VisualStudio.TestTools.UnitTesting;
using SimpleReactionMachine;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;

namespace EnhancedSimpleReactionControllerTests
{
    [TestClass]
    public class Tester
    {
        private EnhancedReactionController controller;
        private DummyGui gui;
        private RndGenerator rng;

        [TestInitialize]
        public void Setup()
        {
            controller = new EnhancedReactionController();
            gui = new DummyGui();
            rng = new RndGenerator();
            gui.Connect(controller);
            controller.Connect(gui, rng);
        }

        // Test case: Create controller
        [TestMethod]
        public void TestCreateController()
        {
            Assert.IsNotNull(controller);
        }

        // Test case: Connect and initialize controller
        [TestMethod]
        public void TestConnectAndInitializeController()
        {
            controller.Init();
            Assert.AreEqual("Insert coin", gui.DisplayText);
        }

        // Test case: Coin inserted without start
        [TestMethod]
        public void TestCoinInsertedWithoutStart()
        {
            controller.Init();
            controller.CoinInserted();
            Assert.AreEqual("Press Go", gui.DisplayText);
        }

        // Test case: Game over after 10 seconds of inactivity
        [TestMethod]
        public void TestGameOverAfter10Seconds()
        {
            controller.Init();
            controller.CoinInserted();
            Thread.Sleep(11000); // This sleep simulates waiting for the inactivity period
            Assert.AreEqual("Insert coin", gui.DisplayText);
        }

        // Test case: Abort game during waiting period
        [TestMethod]
        public void TestAbortGameDuringWaitingPeriod()
        {
            controller.Init();
            controller.CoinInserted();
            controller.GoStopPressed(); // Start waiting for random delay
            Thread.Sleep(2000);
            controller.GoStopPressed(); // Abort the game
            Assert.AreEqual("Insert coin", gui.DisplayText);
        }

        // Test case: Abort game during display time
        [TestMethod]
        public void TestAbortGameDuringDisplayTime()
        {
            controller.Init();
            controller.CoinInserted();
            controller.GoStopPressed(); // Start waiting for random delay
            Thread.Sleep(3000);
            controller.GoStopPressed(); // Display reaction time
            Thread.Sleep(1000); // Allow some time for the display to show reaction time
            controller.GoStopPressed(); // Abort the game
            Assert.AreEqual("Insert coin", gui.DisplayText);
        }

        // Test case: Play multiple games
        [TestMethod]
        public void TestPlayMultipleGames()
        {
            controller.Init();
            controller.CoinInserted();
            for (int i = 0; i < 3; i++)
            {
                controller.GoStopPressed(); // Start waiting for random delay
                Thread.Sleep(3000);
                controller.GoStopPressed(); // Display reaction time
                Thread.Sleep(1000); // Allow some time for the display to show reaction time
            }
            Thread.Sleep(1000); // Allow some time for the display to show average
            Assert.IsTrue(gui.DisplayText.StartsWith("Average ="));
        }

        // Test case: Abort game during average display
        [TestMethod]
        public void TestAbortGameDuringAverageDisplay()
        {
            controller.Init();
            controller.CoinInserted();
            for (int i = 0; i < 3; i++)
            {
                controller.GoStopPressed(); // Start waiting for random delay
                Thread.Sleep(3000);
                controller.GoStopPressed(); // Display reaction time
                Thread.Sleep(1000); // Allow some time for the display to show reaction time
            }
            Thread.Sleep(2000); // Allow some time for the display to show average
            controller.GoStopPressed(); // Abort the game
            Assert.AreEqual("Insert coin", gui.DisplayText);
        }
    }

    public class DummyGui : IGui
    {
        public IController Controller { get; private set; }
        public string DisplayText { get; private set; }

        public void Connect(IController controller)
        {
            Controller = controller;
        }

        public void Init()
        {
            DisplayText = "?reset?";
        }

        public void SetDisplay(string msg)
        {
            DisplayText = msg;
        }
    }

    public class RndGenerator : IRandom
    {
        private readonly System.Random rnd = new System.Random();

        public int GetRandom(int from, int to)
        {
            return rnd.Next(from, to);
        }
    }
}
