import streamlit as st
import pandas as pd # Dodano pandas dla lepszego wyświetlania tabelarycznego

# --- Inicjalizacja Magazynu (Resetowana przy każdej interakcji) ---
# Używamy słownika: {Nazwa Towaru: Ilość Sztuk}
inventory = {
    "Kawa": 50,
    "Herbata": 120,
    "Cukier": 35,
    "Mleko": 70
}

# --- Interfejs Użytkownika Streamlit ---

st.title("🗑️ Magazyn Mateusza")
st.markdown("Dane są resetowane po każdej interakcji, ponieważ nie używa się sesji/plików.")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")

# Uwaga: W tym uproszczonym modelu dodajemy tylko nowy klucz (nazwę) z domyślną ilością.
with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        new_item = st.text_input("Nazwa Nowego Towaru", key="new_item_name")
    with col2:
        # Możemy dodać możliwość wpisania ilości, ale ze względu na reset, ma to ograniczoną funkcjonalność
        new_quantity = st.number_input("Ilość", min_value=1, value=10, step=1, key="new_item_qty")

    submitted_add = st.form_submit_button("Dodaj (Tymczasowo)")
    
    if submitted_add and new_item.strip():
        item_name = new_item.strip()
        if item_name not in inventory:
            inventory[item_name] = new_quantity # Dodanie do słownika
            st.success(f"Dodano do tymczasowej listy: **{item_name}** ({new_quantity} szt.)")
        else:
            # W uproszczonym modelu, jeśli towar istnieje, informujemy, ale nie zmieniamy ilości.
            st.warning(f"Towar **{item_name}** już istnieje. Ilość pozostaje bez zmian.")
    elif submitted_add and not new_item.strip():
        st.error("Wprowadź nazwę towaru.")

# --- Separator ---
st.markdown("---")

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

item_names = list(inventory.keys())

if item_names:
    item_to_remove = st.selectbox(
        "Wybierz towar do usunięcia",
        options=item_names
    )
    
    if st.button("Usuń Wybrany Towar (Tymczasowo)"):
        try:
            del inventory[item_to_remove] # Usuwanie klucza ze słownika
            st.warning(f"Usunięto z tymczasowej listy: **{item_to_remove}**")
        except KeyError:
            st.error("Błąd usuwania.")
else:
    st.info("Lista jest pusta.")

# --- Separator ---
st.markdown("---")

# --- Wyświetlanie Aktualnych Stanów Magazynowych ---
st.header("📋 Aktualne Stany Magazynowe")

if inventory:
    # Konwersja słownika na DataFrame do ładniejszego wyświetlania
    inventory_df = pd.DataFrame(
        list(inventory.items()), 
        columns=["Nazwa Towaru", "Ilość Sztuk"]
    )
    
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)
else:
    st.write("**Magazyn jest pusty!**")


# --- Nowa Lubryka: Całkowite Stany Magazynowe ---
st.header("📊 Całkowite Stan Magazynowy (Suma Sztuk)")

total_items_count = sum(inventory.values())
total_unique_products = len(inventory)

st.metric(
    label="Całkowita Liczba Sztuk (Wszystkie Produkty)", 
    value=f"{total_items_count} szt."
)

st.info(f"Całkowita liczba **unikalnych produktów**: **{total_unique_products}**")


st.warning("Pamiętaj: Jakakolwiek interakcja (np. dodanie/usunięcie) **resetuje** listę do stanu początkowego z kodzie (`Kawa: 50, Herbata: 120` itd.).")
