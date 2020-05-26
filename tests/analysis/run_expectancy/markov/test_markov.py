import pytest

from pybaseballdatana.analysis.simulations import (
    GameState,
    BattingEvent,
    BattingEventProbability,
    BaseOutState,
    BaseState,
    RunEventProbability,
    GameEvent,
    Lineup,
    Batter,
)
from pybaseballdatana.analysis.run_expectancy.markov import (
    MarkovSimulation,
    MarkovState,
    MarkovEvent,
    MarkovEvents,
)


def test_markov_simulation_transitions():
    markov_simulation = MarkovSimulation()

    initial_state = MarkovState(
        game_state=GameState(
            BaseOutState(BaseState(0, 0, 0), outs=0), lineup_slot=1, pa_count=1
        ),
        probability=1,
    )
    event = MarkovEvent(game_event=GameEvent(BattingEvent.OUT), probability=1)
    expected_state = MarkovState(
        game_state=GameState(
            base_out_state=BaseOutState(base_state=BaseState(0, 0, 0), outs=1),
            lineup_slot=2,
            pa_count=2,
        ),
        probability=1,
    )
    assert markov_simulation.state_transition(initial_state, event) == expected_state

    initial_state = MarkovState(
        game_state=GameState(
            BaseOutState(BaseState(0, 0, 0), outs=0), lineup_slot=1, pa_count=1
        ),
        probability=1,
    )
    event = MarkovEvent(game_event=GameEvent(BattingEvent.HOME_RUN), probability=1)
    expected_state = MarkovState(
        game_state=GameState(
            base_out_state=BaseOutState(base_state=BaseState(0, 0, 0), outs=0),
            lineup_slot=2,
            pa_count=2,
            score=1,
        ),
        probability=1,
    )
    assert markov_simulation.state_transition(initial_state, event) == expected_state

    initial_state = MarkovState(
        game_state=GameState(
            BaseOutState(BaseState(0, 0, 0), outs=0), lineup_slot=1, pa_count=1
        ),
        probability=0.5,
    )
    event = MarkovEvent(game_event=GameEvent(BattingEvent.HOME_RUN), probability=1)
    expected_state = MarkovState(
        game_state=GameState(
            base_out_state=BaseOutState(base_state=BaseState(0, 0, 0), outs=0),
            lineup_slot=2,
            pa_count=2,
            score=1,
        ),
        probability=0.5,
    )
    assert markov_simulation.state_transition(initial_state, event) == expected_state


def test_markov_events():
    _ = MarkovEvents([MarkovEvent(GameEvent(BattingEvent.SINGLE), 1)])

    be = BattingEventProbability(0.08, 0.15, 0.05, 0.005, 0.03)
    re = RunEventProbability(0, 0, 0, 0)
    markov_events = MarkovEvents.from_probs(be, re)
    assert markov_events.total_probability == 1

    be = BattingEventProbability(0.08, 0.15, 0.05, 0.005, 0.03)
    re = RunEventProbability(0.1, 0.1, 0.1, 0.1)
    markov_events = MarkovEvents.from_probs(be, re)
    assert markov_events.total_probability == 1


def test_markov_step():
    markov_simulation = MarkovSimulation()
    state_vector = markov_simulation.state_vector
    be = BattingEventProbability(0.08, 0.15, 0.05, 0.005, 0.03)
    re = RunEventProbability(0.1, 0.1, 0.1, 0.1)
    markov_events = MarkovEvents.from_probs(be, re)

    for expected_lineup_slot in range(1, 10):
        assert state_vector.lineup_slot == expected_lineup_slot
        state_vector = markov_simulation.markov_step(state_vector, markov_events)

    for expected_lineup_slot in range(1, 10):
        assert state_vector.lineup_slot == expected_lineup_slot
        state_vector = markov_simulation.markov_step(state_vector, markov_events)

    markov_simulation.markov_step(state_vector, markov_events, num_processes=2)
    markov_simulation.markov_step(state_vector, markov_events, num_processes=1)


def test_markov_simulations_results():
    markov_simulation = MarkovSimulation(termination_threshold=1e-4)

    batting_event_probs = BattingEventProbability(0, 0, 0, 0, 0)
    running_event_probs = RunEventProbability(0, 0, 0, 0)
    batter = Batter(player_id="abc123", event_probabilities=batting_event_probs)
    lineup = Lineup(lineup=[batter] * 9)
    result = markov_simulation(lineup)
    assert result[-1].mean_score == pytest.approx(0)

    batting_event_probs = BattingEventProbability(0.5, 0, 0, 0, 0)
    running_event_probs = RunEventProbability(0, 0, 0, 0)
    batter = Batter(player_id="abc123", event_probabilities=batting_event_probs)
    lineup = Lineup(lineup=[batter] * 9)
    result = markov_simulation(lineup)
    assert result[-1].mean_score == pytest.approx(0.9375, 0.01)

    batting_event_probs = BattingEventProbability(0, 0, 0, 0, 0.5)
    running_event_probs = RunEventProbability(0, 0, 0, 0)
    batter = Batter(player_id="abc123", event_probabilities=batting_event_probs)
    lineup = Lineup(lineup=[batter] * 9)
    result = markov_simulation(lineup)
    assert result[-1].mean_score == pytest.approx(3, 0.01)

    other_batter = Batter(player_id="xyz789", event_probabilities=batting_event_probs)
    other_batter.set_event_probs(home_run=0)
    lineup.set_lineup_slot(1, other_batter)
    result = markov_simulation(lineup)
    assert result[-1].mean_score < 3
