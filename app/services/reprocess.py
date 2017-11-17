
class ReprocessService:

    def __init__(self, ore_calc):
        self.ore_calc = ore_calc


    def only_minerals(self):
        pass


    def reprocess(self):

        result = {}
        queue = {}
        process = {}

        for item in self.ore_calc.build_items:
            process[item.type_id] = {

            }

        while True:


            if len(process) == 0:
                break
            else:
                queue = process
                process = {}


        return result