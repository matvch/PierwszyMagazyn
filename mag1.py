import streamlit as st

# --- Inicjalizacja Magazynu (Resetowana przy każdej interakcji) ---
inventory = [
    "Kawa", 
    "Herbata", 
    "Cukier",
    "Mleko"
]

# --- Interfejs Użytkownika Streamlit ---

st.title("🗑️ Magazyn Mateusza")
st.markdown("Lista jest resetowana po każdej interakcji, ponieważ nie używa ani sesji, ani plików.")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")
with st.form("add_form", clear_on_submit=True):
    new_item = st.text_input("Nazwa Towaru")
    submitted_add = st.form_submit_button("Dodaj (Tymczasowo)")
    
    if submitted_add and new_item.strip():
        inventory.append(new_item.strip())
        st.success(f"Dodano do tymczasowej listy: **{new_item.strip()}**")
    elif submitted_add and not new_item.strip():
        st.error("Wprowadź nazwę towaru.")

# --- Separator ---
st.markdown("---")

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

if inventory:
    # Wyświetlamy obecny stan listy, który może nie uwzględniać zmian z poprzedniego kliknięcia
    item_to_remove = st.selectbox(
        "Wybierz towar do usunięcia",
        options=inventory
    )
    
    if st.button("Usuń Wybrany Towar (Tymczasowo)"):
        try:
            inventory.remove(item_to_remove)
            st.warning(f"Usunięto z tymczasowej listy: **{item_to_remove}**")
        except ValueError:
            st.error("Błąd usuwania.")
else:
    st.info("Lista jest pusta.")

# --- Separator ---
st.markdown("---")

# --- Wyświetlanie Aktualnej Listy ---
st.header("📋 Aktualna Lista w Skrypcie")
st.write(inventory) 
st.info(f"Całkowita liczba towarów: **{len(inventory)}**")

st.warning("Jeśli klikniesz jakikolwiek przycisk, ta lista zostanie zresetowana do stanu początkowego 'Kawa', 'Herbata', 'Cukier', 'Mleko'.")
