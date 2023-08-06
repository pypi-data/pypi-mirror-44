from invoke import task, Collection
from magicinvoke import magictask

ns = Collection()

@ns.magictask
def mine(ctx, output_path=None):
    print(ctx)
    print(output_path + '')
    pass

@task(mine)
def mytask(ctx):
    pass


# Used to test error msgs
ns.configure({"tasks": {"mine": {"output_path": lambda ctx: "/dev/null"}}})
#ns.configure({"tasks": {"mine": lambda ctx: 2+{"output_path": lambda ctx: "/dev/null"}}})
