using SimpleReactionMachine;
using System;
using System.Collections.Generic;
using System.Diagnostics;

public class EnhancedReactionController : IController
{
    private IGui gui;
    private IRandom rng;
    private int gameCount;
    private int maxGames;
    private Stopwatch stopwatch;
    private List<double> reactionTimes;
    private State currentState;

    private enum State
    {
        Idle,
        CoinInserted,
        WaitingForStart,
        DisplayingReactionTime,
        WaitingForNextGame,
        DisplayingAverage
    }

    public void Connect(IGui gui, IRandom rng)
    {
        this.gui = gui;
        this.rng = rng;
        this.gui.Connect(this);
    }

    public void Init()
    {
        gameCount = 0;
        maxGames = 3;
        reactionTimes = new List<double>();
        currentState = State.Idle;
        gui.SetDisplay("Insert coin");
    }

    public void CoinInserted()
    {
        if (currentState == State.Idle)
        {
            currentState = State.CoinInserted;
            gui.SetDisplay("Press Go");
        }
    }

    public void GoStopPressed()
    {
        switch (currentState)
        {
            case State.CoinInserted:
                currentState = State.WaitingForStart;
                int delay = rng.GetRandom(2, 5);
                stopwatch = Stopwatch.StartNew();
                System.Threading.Timer timer = null;
                timer = new System.Threading.Timer(_ =>
                {
                    stopwatch.Stop();
                    double reactionTime = stopwatch.Elapsed.TotalSeconds;
                    reactionTimes.Add(reactionTime);
                    currentState = State.DisplayingReactionTime;
                    gui.SetDisplay(reactionTime.ToString("0.00"));
                    timer.Dispose();
                }, null, delay * 1000, System.Threading.Timeout.Infinite);
                break;

            case State.WaitingForStart:
                currentState = State.Idle;
                gui.SetDisplay("Insert coin");
                break;

            case State.DisplayingReactionTime:
                gameCount++;
                if (gameCount == maxGames)
                {
                    currentState = State.DisplayingAverage;
                    double average = reactionTimes.Count > 0 ? reactionTimes.Average() : 0;
                    gui.SetDisplay($"Average = {average:0.00}");
                    System.Threading.Timer averageTimer = null;
                    averageTimer = new System.Threading.Timer(_ =>
                    {
                        currentState = State.Idle;
                        gui.SetDisplay("Insert coin");
                        averageTimer.Dispose();
                    }, null, 5000, System.Threading.Timeout.Infinite);
                }
                else
                {
                    currentState = State.WaitingForNextGame;
                    gui.SetDisplay("Wait...");
                    int nextDelay = rng.GetRandom(2, 5);
                    System.Threading.Timer nextTimer = null;
                    nextTimer = new System.Threading.Timer(_ =>
                    {
                        currentState = State.WaitingForStart;
                        gui.SetDisplay("Press Go");
                        nextTimer.Dispose();
                    }, null, nextDelay * 1000, System.Threading.Timeout.Infinite);
                }
                break;

            case State.WaitingForNextGame:
            case State.DisplayingAverage:
                currentState = State.Idle;
                gui.SetDisplay("Insert coin");
                break;
        }
    }

    public void Tick()
    {
        throw new NotImplementedException();
    }

    public void Initialize()
    {
        throw new NotImplementedException();
    }
}