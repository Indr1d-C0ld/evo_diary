# ui/main_menu.py
from db.queries import insert_note, list_notes, search_notes, insert_tags, insert_link
from analysis.nlp import extract_keywords
from analysis.related import find_related_notes
from analysis.trends import suggest_next_topic
from ai.models import suggest_category, train_model

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def main_menu():
    while True:
        console.clear()
        console.rule("[bold blue]Diario Personale[/bold blue]")
        console.print("1. Inserisci una nuova nota")
        console.print("2. Visualizza tutte le note")
        console.print("3. Cerca una nota")
        console.print("4. Esci")
        console.print("5. Suggerimenti")
        console.print("6. Addestra il modello di categorizzazione (se hai note già categorizzate)")

        choice = Prompt.ask("Seleziona un'opzione", choices=["1","2","3","4","5","6"])
        
        if choice == '1':
            text = Prompt.ask("Inserisci il testo della nota")
            # Suggerisci una categoria (se il modello è addestrato)
            suggested = suggest_category(text)
            if suggested:
                console.print(f"[blue]Suggerimento di categoria: {suggested}[/blue]")
            category = Prompt.ask("Categoria (opzionale)", default=suggested if suggested else "")
            note_id = insert_note(text, category)
            keywords = extract_keywords(text, language='italian')
            if keywords:
                insert_tags(note_id, keywords)

            # Trova note correlate
            related = find_related_notes(note_id)
            for r_id in related:
                insert_link(note_id, r_id)
            
            console.print("[green]Nota, tag e collegamenti aggiunti con successo![/green]")
            Prompt.ask("Premi invio per continuare")
        
        elif choice == '2':
            notes = list_notes()
            table = Table(title="Tutte le Note")
            table.add_column("ID", style="dim")
            table.add_column("Timestamp")
            table.add_column("Categoria", style="cyan")
            table.add_column("Testo", style="magenta")

            for n in notes:
                short_text = n[2] if len(n[2])<=50 else n[2][:50]+"..."
                table.add_row(str(n[0]), str(n[1]), str(n[3]), short_text)
            console.print(table)
            Prompt.ask("Premi invio per continuare")
        
        elif choice == '3':
            keyword = Prompt.ask("Inserisci keyword per la ricerca")
            results = search_notes(keyword)
            if results:
                table = Table(title=f"Risultati della ricerca per '{keyword}'")
                table.add_column("ID", style="dim")
                table.add_column("Timestamp")
                table.add_column("Categoria", style="cyan")
                table.add_column("Testo", style="magenta")
                for r in results:
                    short_text = r[2] if len(r[2])<=50 else r[2][:50]+"..."
                    table.add_row(str(r[0]), str(r[1]), str(r[3]), short_text)
                console.print(table)
            else:
                console.print("[yellow]Nessun risultato trovato.[/yellow]")
            Prompt.ask("Premi invio per continuare")
        
        elif choice == '4':
            console.print("[bold red]Uscita...[/bold red]")
            break

        elif choice == '5':
            suggestion = suggest_next_topic()
            if suggestion:
                console.print(f"[blue]{suggestion}[/blue]")
            else:
                console.print("Nessun suggerimento disponibile.")
            Prompt.ask("Premi invio per continuare")

        elif choice == '6':
            path = train_model()
            if path:
                console.print("[green]Modello addestrato con successo![/green]")
            else:
                console.print("[red]Non ci sono sufficienti dati per addestrare il modello.[/red]")
            Prompt.ask("Premi invio per continuare")
