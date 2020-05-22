import attr
from typing import List
from pybaseballdatana.analysis.simulations.components.event import (
    BattingEvent,
    FirstBaseRunningEvent,
    SecondBaseRunningEvent,
    ThirdBaseRunningEvent,
)
from pybaseballdatana.analysis.simulations.components.player import Batter
from pybaseballdatana.analysis.utils import check_len, check_is_zero_one
from functools import partial, lru_cache


@attr.s(frozen=True)
class BaseState:
    first_base = attr.ib(type=int, validator=check_is_zero_one)
    second_base = attr.ib(type=int, validator=check_is_zero_one)
    third_base = attr.ib(type=int, validator=check_is_zero_one)

    def __iter__(self):
        yield self.first_base
        yield self.second_base
        yield self.third_base


@lru_cache(maxsize=1024)
def base_out_state_evolve_cached(
    cls,
    batting_event,
    first_base_running_event=FirstBaseRunningEvent.DEFAULT,
    second_base_running_event=SecondBaseRunningEvent.DEFAULT,
    third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
):
    return cls.evolve(
        batting_event,
        first_base_running_event=first_base_running_event,
        second_base_running_event=second_base_running_event,
        third_base_running_event=third_base_running_event,
    )


@lru_cache(maxsize=1024)
def runs_scored_cached(initial_state, end_state):
    return BaseOutState.runs_scored(initial_state, end_state)


@lru_cache(maxsize=1024)
def get_running_events_cached(
    batting_event,
    first_base_running_event,
    second_base_running_event,
    third_base_running_event,
):
    return BaseOutState.get_running_events(
        batting_event,
        first_base_running_event,
        second_base_running_event,
        third_base_running_event,
    )


@lru_cache(maxsize=1024)
def validate_running_events_cached(
    first_base_running_event, second_base_running_event, third_base_running_event
):
    return BaseOutState._validate_running_events(
        first_base_running_event, second_base_running_event, third_base_running_event
    )


@attr.s(frozen=True)
class BaseOutState:
    base_state = attr.ib(type=BaseState)
    outs = attr.ib(type=int)

    @staticmethod
    def runs_scored(initial_state, end_state):
        # runs = -d(runners) - d(outs) + 1
        if end_state.outs == 3:
            return 0
        runners_end = sum(end_state.base_state)
        runners_start = sum(initial_state.base_state)
        delta_runners = runners_end - runners_start
        delta_outs = end_state.outs - initial_state.outs
        return 1 - delta_runners - delta_outs

    @staticmethod
    def get_running_events(
        batting_event,
        first_base_running_event,
        second_base_running_event,
        third_base_running_event,
    ):
        if batting_event == BattingEvent.SINGLE:
            running_events = (
                (
                    FirstBaseRunningEvent.FIRST_TO_SECOND
                    if first_base_running_event == FirstBaseRunningEvent.DEFAULT
                    else first_base_running_event
                ),
                (
                    SecondBaseRunningEvent.SECOND_TO_THIRD
                    if second_base_running_event == SecondBaseRunningEvent.DEFAULT
                    else second_base_running_event
                ),
                (
                    ThirdBaseRunningEvent.THIRD_TO_HOME
                    if third_base_running_event == ThirdBaseRunningEvent.DEFAULT
                    else third_base_running_event
                ),
            )
        elif batting_event == BattingEvent.DOUBLE:
            running_events = (
                (
                    FirstBaseRunningEvent.FIRST_TO_THIRD
                    if first_base_running_event == FirstBaseRunningEvent.DEFAULT
                    else first_base_running_event
                ),
                (
                    SecondBaseRunningEvent.SECOND_TO_HOME
                    if second_base_running_event == SecondBaseRunningEvent.DEFAULT
                    else second_base_running_event
                ),
                (
                    ThirdBaseRunningEvent.THIRD_TO_HOME
                    if third_base_running_event == ThirdBaseRunningEvent.DEFAULT
                    else third_base_running_event
                ),
            )
        else:
            running_events = (
                first_base_running_event,
                second_base_running_event,
                third_base_running_event,
            )
        BaseOutState._validate_running_events(*running_events)
        return running_events

    @staticmethod
    def _validate_running_events(
        first_base_running_event, second_base_running_event, third_base_running_event
    ):
        if (
            first_base_running_event == FirstBaseRunningEvent.FIRST_TO_THIRD
            or first_base_running_event == FirstBaseRunningEvent.FIRST_TO_HOME
        ) and second_base_running_event != SecondBaseRunningEvent.SECOND_TO_HOME:
            raise ValueError(
                "running events are not consistent %s",
                (
                    first_base_running_event,
                    second_base_running_event,
                    third_base_running_event,
                ),
            )

    def evolve(
        self,
        batting_event,
        first_base_running_event=FirstBaseRunningEvent.DEFAULT,
        second_base_running_event=SecondBaseRunningEvent.DEFAULT,
        third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
    ):

        outs = self.outs
        base_state = attr.evolve(self.base_state)

        if outs == 3:
            pass

        elif batting_event == BattingEvent.OUT:
            outs = self.outs + 1

        elif batting_event == BattingEvent.BASE_ON_BALLS:
            base_state = BaseState(
                first_base=1,
                second_base=1
                if self.base_state.first_base == 1
                else self.base_state.second_base,
                third_base=1
                if self.base_state.first_base == 1 and self.base_state.second_base == 1
                else self.base_state.third_base,
            )

        elif batting_event == BattingEvent.SINGLE:

            running_events = self.get_running_events(
                batting_event,
                first_base_running_event,
                second_base_running_event,
                third_base_running_event,
            )[0:2]

            if running_events == (
                FirstBaseRunningEvent.FIRST_TO_SECOND,
                SecondBaseRunningEvent.SECOND_TO_THIRD,
            ):
                base_state = BaseState(
                    1,
                    1 if self.base_state.first_base else 0,
                    1 if self.base_state.second_base else 0,
                )

            elif running_events == (
                FirstBaseRunningEvent.FIRST_TO_SECOND,
                SecondBaseRunningEvent.SECOND_TO_HOME,
            ):
                base_state = BaseState(1, 1 if self.base_state.first_base else 0, 0)

            elif running_events == (
                FirstBaseRunningEvent.FIRST_TO_THIRD,
                SecondBaseRunningEvent.SECOND_TO_HOME,
            ):
                base_state = BaseState(1, 0, 1 if self.base_state.first_base else 0)

            elif running_events == (
                FirstBaseRunningEvent.FIRST_TO_HOME,
                SecondBaseRunningEvent.SECOND_TO_HOME,
            ):
                base_state = BaseState(1, 0, 0)

            else:
                raise ValueError(
                    "running_events combination %s is not valid", running_events
                )
        elif batting_event == BattingEvent.DOUBLE:
            running_events = self.get_running_events(
                batting_event,
                first_base_running_event,
                second_base_running_event,
                third_base_running_event,
            )[0]

            if running_events == FirstBaseRunningEvent.FIRST_TO_THIRD:
                base_state = BaseState(0, 1, 1 if self.base_state.first_base else 0)
            elif running_events == FirstBaseRunningEvent.FIRST_TO_HOME:
                base_state = BaseState(0, 1, 0)

        elif batting_event == BattingEvent.TRIPLE:
            base_state = BaseState(0, 0, 1)
        elif batting_event == BattingEvent.HOME_RUN:
            base_state = BaseState(0, 0, 0)
        else:
            raise ValueError(
                "evolving with batting event {} "
                "and running events %{} is not valid".format(
                    batting_event,
                    (
                        first_base_running_event,
                        second_base_running_event,
                        third_base_running_event,
                    ),
                )
            )

        return attr.evolve(self, base_state=base_state, outs=outs)


@attr.s
class Lineup:
    lineup = attr.ib(List[Batter], validator=partial(check_len, len_constraint=9))


@lru_cache(maxsize=1024)
def game_state_evolve_cached(
    cls,
    batting_event,
    first_base_running_event=FirstBaseRunningEvent.DEFAULT,
    second_base_running_event=SecondBaseRunningEvent.DEFAULT,
    third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
):
    return GameState.evolve(
        cls,
        batting_event,
        first_base_running_event,
        second_base_running_event,
        third_base_running_event,
    )


@attr.s(hash=True)
class GameState:
    base_out_state = attr.ib(
        type=BaseOutState, default=BaseOutState(BaseState(0, 0, 0), 0)
    )
    pa_count = attr.ib(type=int, default=1)
    lineup_slot = attr.ib(type=int, default=1)
    score = attr.ib(type=int, default=0)

    def evolve(
        self,
        batting_event,
        first_base_running_event=FirstBaseRunningEvent.DEFAULT,
        second_base_running_event=SecondBaseRunningEvent.DEFAULT,
        third_base_running_event=ThirdBaseRunningEvent.DEFAULT,
    ):
        base_out_state = self.base_out_state.evolve(
            batting_event,
            first_base_running_event,
            second_base_running_event,
            third_base_running_event,
        )
        runs_scored = BaseOutState.runs_scored(self.base_out_state, base_out_state)
        game_state = attr.evolve(
            self,
            base_out_state=base_out_state,
            pa_count=self.pa_count + 1,
            lineup_slot=self.lineup_slot + 1,
            score=self.score + runs_scored,
        )

        return game_state
