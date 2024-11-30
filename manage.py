import click
from vendor.Cli.core import *
from Rocket import *
from final import MainApp


@click.group()
def cli():
    pass


@cli.command()
def cleanup():
    "Clean up app the temp files"

    #files that you want ot delete
    files_to_remove = ["main.spec"]
    
    #Dir that you want ot delete
    dir_to_remove = ["__pycache__","dist","build"]
    file_end_with=[".spec"]
    cleanup_(files_to_remove,dir_to_remove)


@cli.command()
def Cleanbuilt()-> None:
    pass


@cli.command()
@click.option('-o', '--onefile', 
              is_flag=True, 
              help="Build a single-file executable.")
def built(onefile: bool) -> None:
    """
    Build the application as an executable. Optionally build a single-file executable.
    """
    try:
        create_executable(onefile=onefile, output_dir="./build")
        print("Build completed successfully.")
    except Exception as e:
        print(f"Build failed: {e}")
    return


@cli.command()
@click.option('-c', '--clean', 
            is_flag=True, 
            help="Clean up before running the application.",)
def Run(clean:bool)->None:
    if clean:
        cleanup_([],["__pycache__","build"])
    MainApp()


@cli.command()
def  version()->None:
    print(VERSION)
    return


if __name__ == "__main__":
    cli()