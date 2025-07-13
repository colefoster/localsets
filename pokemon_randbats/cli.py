"""
Command line interface for pokemon-randbats.
"""

import click
import json
import logging
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from .core import RandBatsData
from .formats import FORMATS, FORMAT_MAPPINGS, resolve_formats, get_format_info

console = Console()


def setup_logging(verbose: bool):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def main(ctx, verbose):
    """Pokemon Random Battle Data CLI."""
    setup_logging(verbose)
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@main.command()
@click.option('--format', '-f', 'format_name', help='Specific format to update')
@click.option('--all', 'update_all', is_flag=True, help='Update all formats')
@click.option('--force', is_flag=True, help='Force update even if no changes detected')
@click.pass_context
def update(ctx, format_name, update_all, force):
    """Update Pokemon random battle data."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Initializing...", total=None)
        
        try:
            data = RandBatsData(auto_update=False)
            
            if update_all:
                formats_to_update = FORMATS
                progress.update(task, description="Updating all formats...")
            elif format_name:
                formats_to_update = resolve_formats([format_name])
                progress.update(task, description=f"Updating {format_name}...")
            else:
                formats_to_update = data.get_formats()
                progress.update(task, description="Updating loaded formats...")
            
            if not formats_to_update:
                console.print("[yellow]No formats to update[/yellow]")
                return
            
            if force:
                updated = data.updater.force_update(formats_to_update)
            else:
                updated = data.updater.update_formats(formats_to_update)
            
            if updated:
                console.print(f"[green]✓ Updated {len(updated)} formats: {', '.join(updated)}[/green]")
            else:
                console.print("[yellow]No updates needed[/yellow]")
                
        except Exception as e:
            console.print(f"[red]Update failed: {e}[/red]")
            raise click.Abort()


@main.command()
@click.argument('pokemon_name')
@click.option('--format', '-f', 'format_name', help='Specific format to search in')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def get(ctx, pokemon_name, format_name, output_json):
    """Get Pokemon data."""
    try:
        data = RandBatsData()
        pokemon_data = data.get_pokemon(pokemon_name, format_name)
        
        if pokemon_data is None:
            console.print(f"[red]Pokemon '{pokemon_name}' not found[/red]")
            raise click.Abort()
        
        if output_json:
            console.print(json.dumps(pokemon_data, indent=2))
        else:
            display_pokemon_data(pokemon_data, pokemon_name, format_name)
            
    except Exception as e:
        console.print(f"[red]Failed to get Pokemon data: {e}[/red]")
        raise click.Abort()


@main.command()
@click.option('--format', '-f', 'format_name', help='Specific format to list')
@click.option('--count', is_flag=True, help='Show only count')
@click.pass_context
def list(ctx, format_name, count):
    """List Pokemon in format(s)."""
    try:
        data = RandBatsData()
        
        if format_name:
            formats_to_list = resolve_formats([format_name])
        else:
            formats_to_list = data.get_formats()
        
        if not formats_to_list:
            console.print("[yellow]No formats available[/yellow]")
            return
        
        if count:
            for fmt in formats_to_list:
                pokemon_list = data.list_pokemon(fmt)
                console.print(f"{fmt}: {len(pokemon_list)} Pokemon")
        else:
            for fmt in formats_to_list:
                pokemon_list = data.list_pokemon(fmt)
                display_pokemon_list(pokemon_list, fmt)
                
    except Exception as e:
        console.print(f"[red]Failed to list Pokemon: {e}[/red]")
        raise click.Abort()


@main.command()
@click.pass_context
def info(ctx):
    """Show package information."""
    try:
        data = RandBatsData()
        cache_info = data.get_cache_info()
        
        # Create info table
        table = Table(title="Pokemon RandBats Info")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Cache Directory", cache_info['cache_dir'])
        table.add_row("Loaded Formats", str(len(cache_info['loaded_formats'])))
        table.add_row("Total Pokemon", str(cache_info['total_pokemon']))
        
        if 'last_update' in cache_info:
            table.add_row("Last Update", cache_info['last_update'])
        
        console.print(table)
        
        # Show format details
        if cache_info['format_counts']:
            format_table = Table(title="Format Details")
            format_table.add_column("Format", style="cyan")
            format_table.add_column("Pokemon Count", style="green")
            
            for fmt, count in cache_info['format_counts'].items():
                format_table.add_row(fmt, str(count))
            
            console.print(format_table)
            
    except Exception as e:
        console.print(f"[red]Failed to get info: {e}[/red]")
        raise click.Abort()


@main.command()
@click.pass_context
def formats(ctx):
    """Show available formats."""
    try:
        table = Table(title="Available Formats")
        table.add_column("Format", style="cyan")
        table.add_column("Generation", style="yellow")
        table.add_column("Type", style="green")
        table.add_column("Description", style="white")
        
        for fmt in FORMATS:
            info = get_format_info(fmt)
            gen = info.get('generation', 'unknown')
            battle_type = info.get('type', 'unknown')
            
            # Generate description
            if 'doubles' in fmt:
                desc = "Double battle format"
            elif 'letsgo' in fmt:
                desc = "Let's Go format"
            elif 'bdsp' in fmt:
                desc = "Brilliant Diamond/Shining Pearl format"
            elif 'baby' in fmt:
                desc = "Baby Pokemon format"
            else:
                desc = f"Generation {gen} random battle"
            
            table.add_row(fmt, gen, battle_type, desc)
        
        console.print(table)
        
        # Show extras mapping
        extras_table = Table(title="Installation Extras")
        extras_table.add_column("Extra", style="cyan")
        extras_table.add_column("Formats", style="green")
        
        for extra, formats_list in FORMAT_MAPPINGS.items():
            if extra != 'all':  # Skip 'all' as it's too long
                extras_table.add_row(extra, ', '.join(formats_list))
        
        console.print(extras_table)
        
    except Exception as e:
        console.print(f"[red]Failed to show formats: {e}[/red]")
        raise click.Abort()


def display_pokemon_data(pokemon_data: dict, pokemon_name: str, format_name: Optional[str]):
    """Display Pokemon data in a formatted way."""
    # Create main panel
    title = f"{pokemon_name.title()}"
    if format_name:
        title += f" ({format_name})"
    
    # Convert data to readable format
    content = []
    for key, value in pokemon_data.items():
        if hasattr(value, '__iter__') and not isinstance(value, (str, dict)):
            content.append(f"[cyan]{key}:[/cyan] {', '.join(map(str, value))}")
        elif isinstance(value, dict):
            content.append(f"[cyan]{key}:[/cyan]")
            for sub_key, sub_value in value.items():
                content.append(f"  {sub_key}: {sub_value}")
        else:
            content.append(f"[cyan]{key}:[/cyan] {value}")
    
    panel = Panel(
        '\n'.join(content),
        title=title,
        border_style="green"
    )
    console.print(panel)


def display_pokemon_list(pokemon_list: List[str], format_name: str):
    """Display Pokemon list in a formatted way."""
    if not pokemon_list:
        console.print(f"[yellow]No Pokemon found in {format_name}[/yellow]")
        return
    
    # Create table
    table = Table(title=f"Pokemon in {format_name}")
    table.add_column("Pokemon", style="cyan")
    
    # Add Pokemon in chunks for better display
    chunk_size = 5
    for i in range(0, len(pokemon_list), chunk_size):
        chunk = pokemon_list[i:i + chunk_size]
        table.add_row(', '.join(chunk))
    
    console.print(table)
    console.print(f"Total: {len(pokemon_list)} Pokemon")


if __name__ == '__main__':
    main() 