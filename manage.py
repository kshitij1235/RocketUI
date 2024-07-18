import click
from vendor.Cli.core import cleanup_

@click.group()
def cli():
    pass

@cli.command()
def cleanup():
    "Clean up app the temp files"

    #files that you want ot delete
    files_to_remove = []
    
    #Dir that you want ot delete
    dir_to_remove = ["__pycache__","dist","build"]
    cleanup_(files_to_remove,dir_to_remove)

@cli.command()
def Cleanbuilt()-> None:
    pass

@cli.command()
def built()-> None:
    pass

@cli.command()
def Run()->None:
    from main import MainApp
    cleanup_([],["__pycache__","dist","build"])
    MainApp()

if __name__ == "__main__":
    cli()