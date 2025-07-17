# seeds/machines.py

from app.models import Machine
from sqlalchemy.orm import Session

def seed_machines(db: Session):
    machines = [
        Machine(
            name="Tennant T300 walk behind scrubber",
            price=3950.00,
            description="Condition Used - like new Tennant T300 brush assist 20 inch scrubber. Only 61 original hours use. All wear items new. New batteries with onboard charger. Works fine new. Free delivery in DFW area. Sweeper floor concrete advance nilfisk powerboss factory cat",
            specifications="n/a",
        ),
        Machine(
            name="Tennant T600",
            price=6500.00,
            description="Condition Used - Good Tennant T600 28 inch scrubber with new pad drivers. Only 203 original hours use. Great condition with slightly used higher capacity batteries. Has onboard charger. Works like new. Free delivery in DFW area. Sweeper scrubber floor concrete advance nilfisk powerboss factory cat Tennant",
            specifications="n/a",
        ),
        Machine(
            name="Advance Tennant CS7010 Sweeper Scrubber",
            price=20000.00,
            description="Condition Used - like New Tennant Advance CS7010 lp powered sweeper scrubber with 1229 original hours use. Built September 2019. Kubota engine run on propane. Everything works as it should and all wear items are new or in good condition. Ready for delivery. Great machine at half what dealer would ask. Sweeps or scrubs separately or all together. Free delivery in Texas by me. OBO!! Tennant factory cat floor concrete powerboss sweeper scrubber",
            specifications="n/a",
        ),
        Machine(
            name="Tennant T16 Sweeper Scrubber",
            price=25000.00,
            description="Condition Used - like New 2021 Tennant T16 with only 48 original hours use. Absolutely like new and works like it too. Just put new larger capacity US 125 batteries in it and installed manual battery fill system. This scrubber has the optional “pre sweep”. Machine can be operated as a sweeper, scrubber or both at the same time. Has lights, back up alarm and clean out hose on back of machine. Works perfectly and almost half price if you include the sweep system OBO free delivery in Texas. Powerboss advance nilfisk floor concrete factory cat sweeper scrubber",
            specifications="n/a",
        )
    ]

    db.add_all(machines)

def undo_machines(db: Session):
    db.query(Machine).delete()