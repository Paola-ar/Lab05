import flet as ft
from alert import AlertManager
# from auton
from autonoleggio import Autonoleggio
from automobile import Automobile

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    input_marca = ft.TextField(label= "Aggiungi Marca")
    input_modello = ft.TextField(label="Aggiungi Modello")
    input_anno = ft.TextField(label="Aggiungi Anno")
    input_posti = ft.TextField(value= "0", disabled = True, border_color="green",width=100,text_align=ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    def aggiungi_auto(e):
        try:
            input_anno.value = int(input_anno.value)
        except Exception as e:
            alert.show_alert(f"❌ {e}")

        autonoleggio.aggiungi_automobile(str(input_marca.value), str(input_modello.value), str(input_anno.value), str(input_posti.value))
        aggiorna_lista_auto()
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def handleAdd(e):
        currentVal = input_posti.value
        input_posti.value = int(currentVal) + 1
        str(input_posti.value)
        input_posti.update()

    def handleRemove(e):
        currentVal = input_posti.value
        input_posti.value = int(currentVal) - 1
        str(input_posti)
        input_posti.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)
    pulsante_aggiunta_auto = ft.ElevatedButton("Aggiungi Automobile", on_click=aggiungi_auto)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    bot_min = ft.IconButton(icon = ft.Icons.REMOVE, icon_color = "red", icon_size = 24, on_click = handleRemove)
    bot_add = ft.IconButton(icon = ft.Icons.ADD, icon_color = "green", icon_size = 24, on_click = handleAdd)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text("Aggiungi Nuova Automobile", size=20),
        ft.Row(spacing=20,
               controls=[input_marca, input_modello, input_anno,bot_min, input_posti, bot_add],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=20,
               controls=[pulsante_aggiunta_auto],
               alignment=ft.MainAxisAlignment.CENTER),

    # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
