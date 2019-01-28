import sc2

from sc2 import run_game, maps, Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer


# All bots inherit from sc2.BotAI
class WorkerRushBot(sc2.BotAI):

    # The on_step function is called for every game step
    # It is defined as async because it calls await functions
    # It takes current game state and current iteration
    async def on_step(self, iteration):
        if iteration == 0:
            await self.do(self.units(UnitTypeId.NEXUS).ready.random.train(UnitTypeId.PROBE))

        if not self.units(UnitTypeId.PYLON).exists and not self.already_pending(UnitTypeId.PYLON):
            if self.can_afford(UnitTypeId.PYLON) and len(self.workers) > 12:
                await self.build(UnitTypeId.PYLON, near=self.units(UnitTypeId.NEXUS).first)

        if len(self.units(UnitTypeId.PYLON)) == 1:
            if self.can_afford(UnitTypeId.GATEWAY) and len(self.units(UnitTypeId.GATEWAY)) == 0:
                await self.build(UnitTypeId.GATEWAY, near=self.units(UnitTypeId.PYLON).first)

        if self.units(UnitTypeId.GATEWAY).exists and not self.already_pending(UnitTypeId.GATEWAY):
            if self.can_afford(UnitTypeId.ZEALOT) and len(self.units(UnitTypeId.ZEALOT)) == 0:
                await self.do(self.units(UnitTypeId.GATEWAY).ready.random.train(UnitTypeId.ZEALOT))

        if len(self.units(UnitTypeId.ZEALOT)) == 1:
            for zealot in self.units(UnitTypeId.ZEALOT):
                await self.do(zealot.attack(self.enemy_start_locations[0]))

        # if iteration == 0:
        #     for worker in self.workers:
        #         await self.do(worker.attack(self.enemy_start_locations[0]))
        #
        # if self.can_afford(UnitTypeId.PROBE):
        #     await self.do(self.units(UnitTypeId.NEXUS).ready.random.train(UnitTypeId.PROBE))
        #
        # if len(self.workers) > 12:
        #     for worker in self.workers:
        #         await self.do(worker.attack(self.enemy_start_locations[0]))


run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Protoss, WorkerRushBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)
