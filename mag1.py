import streamlit as st
import pandas as pd
from collections import Counter

# --- Inicjalizacja Magazynu (Resetowana przy każdej interakcji) ---
# Używamy słownika: {Nazwa Towaru: Ilość Sztuk}
inventory = {
    "Kawa": 50,
    "Herbata": 120,
    "Cukier": 15,  # Zmieniono na 15, żeby przetestować "Zamów Koniecznie"
    "Mleko": 38,   # Zmieniono na 38, żeby przetestować "Blisko Końca"
    "Czekolada": 80
}

# --- FUNKCJA WYZNACZANIA STATUSU ---
def get_order_status(quantity):
    """Zwraca ikonę i kolor statusu zamówienia na podstawie ilości."""
    if quantity <= 20:
        return "🔴 ZAMÓW KONIECZNIE", "low"
    elif quantity <= 40:
        return "🟡 BLISKO KOŃCA", "caution"
    else:
        return "🟢 ODPOWIEDNI STAN", "safe"

# --- Interfejs Użytkownika Streamlit ---

st.title("Magazyn Mateusza 🚚")
st.markdown("Dane są resetowane po każdej interakcji, ponieważ nie używa się sesji/plików.")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")

# Uwaga: W tym uproszczonym modelu dodajemy tylko nowy klucz (nazwę) z domyślną ilością.
with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        new_item = st.text_input("Nazwa Nowego Towaru", key="new_item_name")
    with col2:
        new_quantity = st.number_input("Ilość", min_value=1, value=10, step=1, key="new_item_qty")

    submitted_add = st.form_submit_button("Dodaj (Tymczasowo)")
    
    if submitted_add and new_item.strip():
        item_name = new_item.strip()
        if item_name not in inventory:
            inventory[item_name] = new_quantity
            st.success(f"Dodano do tymczasowej listy: **{item_name}** ({new_quantity} szt.)")
        else:
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
            del inventory[item_to_remove]
            st.warning(f"Usunięto z tymczasowej listy: **{item_to_remove}**")
        except KeyError:
            st.error("Błąd usuwania.")
else:
    st.info("Lista jest pusta.")

# --- Separator ---
st.markdown("---")

# =======================================================
# --- NOWA SEKCJA: STATUS ZAMÓWIEŃ TOWARÓW ---
# =======================================================
st.header("🚨 Status Zamówień Towarów")
st.markdown("Szybki przegląd towarów wymagających uwagi.")

low_stock_items = {k: v for k, v in inventory.items() if v <= 40}

if low_stock_items:
    
    # Sortowanie produktów na 3 kolumny
    col_k, col_b, col_o = st.columns(3)
    
    # 1. ZAMÓW KONIECZNIE (<= 20)
    koniecznie_do_zamowienia = {k: v for k, v in low_stock_items.items() if v <= 20}
    with col_k:
        st.subheader("🔴 Zamów Koniecznie (≤ 20)")
        if koniecznie_do_zamowienia:
            for item, qty in koniecznie_do_zamowienia.items():
                st.error(f"**{item}**: {qty} szt.")
        else:
            st.markdown("Brak towarów poniżej 20 szt.")

    # 2. BLISKO KOŃCA (21 do 40)
    blisko_konca = {k: v for k, v in low_stock_items.items() if 20 < v <= 40}
    with col_b:
        st.subheader("🟡 Blisko Końca (≤ 40)")
        if blisko_konca:
            for item, qty in blisko_konca.items():
                st.warning(f"**{item}**: {qty} szt.")
        else:
            st.markdown("Brak towarów bliskich końca.")

    # 3. ODPOWIEDNI STAN (> 40) - pokazujemy tylko informacyjnie
    odpowiedni_stan = {k: v for k, v in inventory.items() if v > 40}
    with col_o:
        st.subheader("🟢 Odpowiedni Stan (> 40)")
        if odpowiedni_stan:
            st.success(f"Masz **{len(odpowiedni_stan)}** produktów w odpowiednim stanie.")
        else:
            st.info("Brak produktów w wystarczającym stanie.")
            
else:
    st.success("Wszystkie towary są w odpowiednim stanie (powyżej 40 sztuk).")
    
# --- Separator ---
st.markdown("---")

# --- Wyświetlanie Aktualnych Stanów Magazynowych (Zmieniono na sortowanie) ---
st.header("📋 Szczegółowy Raport Magazynowy")

if inventory:
    # Konwersja słownika na DataFrame
    inventory_df = pd.DataFrame(
        list(inventory.items()), 
        columns=["Nazwa Towaru", "Ilość Sztuk"]
    )
    
    # Dodanie kolumny statusu do DataFrame
    inventory_df['Status'] = inventory_df['Ilość Sztuk'].apply(lambda x: get_order_status(x)[0])
    
    st.dataframe(
        inventory_df.sort_values(by='Ilość Sztuk', ascending=True), # Sortowanie od najmniejszej ilości
        use_container_width=True, 
        hide_index=True
    )
else:
    st.write("**Magazyn jest pusty!**")


# --- Nowa Lubryka: Całkowite Stany Magazynowe ---
st.header("📊 Podsumowanie Całkowitego Stanu")

total_items_count = sum(inventory.values())
total_unique_products = len(inventory)

st.metric(
    label="Całkowita Liczba Sztuk (Wszystkie Produkty)", 
    value=f"{total_items_count} szt."
)

st.info(f"Całkowita liczba **unikalnych produktów**: **{total_unique_products}**")

st.warning("Pamiętaj: Jakakolwiek interakcja **resetuje** listę do stanu początkowego (w tym ilości sztuk).")
