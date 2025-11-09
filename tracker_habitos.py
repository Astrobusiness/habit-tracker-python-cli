import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = "habits_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"habits": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"habits": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def pause():
    input("\nPressione ENTER para continuar...")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print("="*50)
    print("   TRACKER DE HÁBITOS - DISCIPLINA DIÁRIA")
    print("="*50)

def calc_streaks(dates):
    from datetime import date, timedelta
    dset = {date.fromisoformat(d) for d in dates}
    if not dset:
        return 0, 0
    dlist = sorted(dset)
    best = 1
    current = 1
    for i in range(1, len(dlist)):
        if dlist[i] - dlist[i-1] == timedelta(days=1):
            current += 1
            if current > best:
                best = current
        else:
            current = 1
    current2 = 1
    ref = dlist[-1]
    for i in range(len(dlist)-2, -1, -1):
        if ref - dlist[i] == timedelta(days=1):
            current2 += 1
            ref = dlist[i]
        else:
            break
    return current2, best

def list_habits(data):
    habits = data.get("habits", {})
    if not habits:
        print("\nNenhum hábito cadastrado ainda.")
        return
    print("\nSeus hábitos:")
    print("-"*50)
    for i, (name, info) in enumerate(habits.items(), start=1):
        logs = info.get("logs", [])
        current_streak, best_streak = calc_streaks(logs)
        print(f"{i}. {name}  |  Categoria: {info.get('category','-')}")
        print(f"   Criado em: {info.get('created_at', '-')}")
        print(f"   Dias concluídos: {len(set(logs))}")
        print(f"   Streak atual: {current_streak}  |  Melhor streak: {best_streak}")
        print("-"*50)

def add_habit(data):
    clear()
    header()
    print("\nNovo hábito")
    name = input("Nome do hábito (ex: Estudar 1h de Python): ").strip()
    if not name:
        print("Nome inválido.")
        return
    if name in data.get("habits", {}):
        print("Já existe um hábito com esse nome.")
        return
    print("\nCategorias sugeridas: Estudo, Treino, Finanças, Saúde, Leitura, Outro")
    category = input("Categoria: ").strip() or "Outro"
    today = date.today().isoformat()
    data["habits"][name] = {
        "category": category,
        "created_at": today,
        "logs": []
    }
    save_data(data)
    print(f"\nHábito '{name}' criado com sucesso!")

def choose_habit(data, prompt="Escolha o número do hábito: "):
    habits = list(data.get("habits", {}).items())
    if not habits:
        print("\nNenhum hábito cadastrado.")
        return None, None
    print("\nHÁBITOS:")
    for i, (name, info) in enumerate(habits, start=1):
        print(f"{i}. {name} ({info.get('category','-')})")
    try:
        choice = int(input(f"\n{prompt}"))
    except ValueError:
        print("Escolha inválida.")
        return None, None
    if 1 <= choice <= len(habits):
        name, info = habits[choice-1]
        return name, info
    else:
        print("Número fora do intervalo.")
        return None, None

def mark_done_today(data):
    clear()
    header()
    name, info = choose_habit(data, "Marcar como concluído hoje - número do hábito: ")
    if not name:
        return
    today = date.today().isoformat()
    logs = info.get("logs", [])
    if today in logs:
        print(f"\nVocê já marcou '{name}' como concluído hoje ({today}).")
        return
    logs.append(today)
    info["logs"] = logs
    data["habits"][name] = info
    save_data(data)
    print(f"\nHábito '{name}' marcado como concluído em {today}!")

def show_stats(data):
    clear()
    header()
    habits = data.get("habits", {})
    if not habits:
        print("\nNenhum hábito cadastrado.")
        return
    print("\nESTATÍSTICAS GERAIS")
    print("-"*50)
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    for name, info in habits.items():
        logs = [date.fromisoformat(d) for d in info.get("logs", [])]
        total_days = len(set(logs))
        current_streak, best_streak = calc_streaks(info.get("logs", []))
        last_30 = [d for d in logs if d >= thirty_days_ago]
        last_30_count = len(set(last_30))
        print(f"Hábito: {name}")
        print(f"  Categoria: {info.get('category','-')}")
        print(f"  Dias concluídos (total): {total_days}")
        print(f"  Conclusões nos últimos 30 dias: {last_30_count}")
        print(f"  Streak atual: {current_streak}")
        print(f"  Melhor streak: {best_streak}")
        print("-"*50)

def delete_habit(data):
    clear()
    header()
    name, info = choose_habit(data, "Número do hábito para excluir: ")
    if not name:
        return
    confirm = input(f"Tem certeza que deseja excluir '{name}'? (s/n): ").strip().lower()
    if confirm == "s":
        data["habits"].pop(name, None)
        save_data(data)
        print("\nHábito excluído com sucesso.")
    else:
        print("\nAção cancelada.")

def main():
    data = load_data()
    while True:
        clear()
        header()
        print("\nMenu:")
        print("1. Listar hábitos")
        print("2. Adicionar novo hábito")
        print("3. Marcar hábito como concluído hoje")
        print("4. Ver estatísticas")
        print("5. Excluir hábito")
        print("0. Sair")
        choice = input("\nEscolha uma opção: ").strip()
        if choice == "1":
            clear()
            header()
            list_habits(data)
            pause()
        elif choice == "2":
            add_habit(data)
            pause()
        elif choice == "3":
            mark_done_today(data)
            pause()
        elif choice == "4":
            show_stats(data)
            pause()
        elif choice == "5":
            delete_habit(data)
            pause()
        elif choice == "0":
            print("\nSaindo... Continue firme na disciplina! :)")
            break
        else:
            print("\nOpção inválida.")
            pause()

if __name__ == "__main__":
    main()
