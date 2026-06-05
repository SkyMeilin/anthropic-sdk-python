#!/usr/bin/env python3
"""
Anthropic SDK Playground - Experimentieren mit KI-Fähigkeiten
Teste verschiedene Möglichkeiten der Anthropic API
"""

import os
from anthropic import Anthropic

def main():
    # Initialisiere den Anthropic Client
    # Stelle sicher, dass ANTHROPIC_API_KEY als Umgebungsvariable gesetzt ist
    client = Anthropic()
    
    print("=" * 60)
    print("Willkommen zum Anthropic SDK Playground!")
    print("Experimentiere mit verschiedenen KI-Fähigkeiten")
    print("=" * 60)
    print()
    
    # Konversationsverlauf speichern für Multi-Turn Conversations
    conversation_history = []
    
    print("Verfügbare Befehle:")
    print("  1. 'chat' - Starte eine interaktive Konversation")
    print("  2. 'test' - Führe verschiedene Test-Prompts aus")
    print("  3. 'exit' - Beende das Programm")
    print()
    
    while True:
        mode = input("Wähle einen Modus (chat/test/exit): ").strip().lower()
        
        if mode == "exit":
            print("Auf Wiedersehen!")
            break
        
        elif mode == "chat":
            chat_mode(client, conversation_history)
        
        elif mode == "test":
            test_mode(client)
        
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")
            print()


def chat_mode(client, conversation_history):
    """Interaktive Konversation mit Claude"""
    print()
    print("--- Chat Modus ---")
    print("Gib 'zurück' ein um zum Hauptmenü zurückzukehren")
    print()
    
    while True:
        user_input = input("Du: ").strip()
        
        if user_input.lower() == "zurück":
            print()
            break
        
        if not user_input:
            continue
        
        # Füge Nachricht zum Verlauf hinzu
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # Sende Nachricht an Claude
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=conversation_history
            )
            
            # Extrahiere Antwort
            assistant_message = response.content[0].text
            
            # Füge Antwort zum Verlauf hinzu
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            print(f"\nClaude: {assistant_message}\n")
            
        except Exception as e:
            print(f"Fehler: {e}")
            # Entferne die letzte Nachricht bei Fehler
            conversation_history.pop()


def test_mode(client):
    """Verschiedene Test-Prompts um KI-Fähigkeiten auszuprobieren"""
    print()
    print("--- Test Modus ---")
    print()
    
    tests = [
        {
            "name": "Kreativität - Gedicht",
            "prompt": "Schreibe ein kurzes, lustiges Gedicht über Programmierung"
        },
        {
            "name": "Analyse - Code Review",
            "prompt": "Analysiere diese Python-Funktion:\n\ndef add(a, b):\n    return a + b\n\nWas könnte man verbessern?"
        },
        {
            "name": "Erklärung - Konzepte",
            "prompt": "Erkläre kurz und verständlich, was Machine Learning ist"
        },
        {
            "name": "Brainstorming - Ideen",
            "prompt": "Gib mir 3 Ideen für kleine Python-Projekte für Anfänger"
        },
        {
            "name": "Problemlösung - Logik",
            "prompt": "Wie würdest du den FizzBuzz-Algorithmus implementieren?"
        },
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"{i}. {test['name']}")
    
    print(f"{len(tests) + 1}. Benutzerdefinierten Prompt eingeben")
    print("0. Zurück zum Hauptmenü")
    print()
    
    choice = input("Wähle einen Test (0-{}): ".format(len(tests) + 1)).strip()
    
    try:
        choice = int(choice)
        
        if choice == 0:
            return
        
        if 1 <= choice <= len(tests):
            prompt = tests[choice - 1]["prompt"]
            test_name = tests[choice - 1]["name"]
        elif choice == len(tests) + 1:
            prompt = input("Gib deinen Prompt ein: ").strip()
            test_name = "Benutzerdefiniert"
        else:
            print("Ungültige Auswahl")
            return
        
        print()
        print(f"Führe aus: {test_name}")
        print("-" * 40)
        
        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = response.content[0].text
            print(result)
            print()
            
        except Exception as e:
            print(f"Fehler bei der API-Anfrage: {e}")
    
    except ValueError:
        print("Ungültige Eingabe")


if __name__ == "__main__":
    main()
