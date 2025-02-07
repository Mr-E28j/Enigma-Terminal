from flask import Flask, render_template, request, jsonify, session
import uuid
import random, base64, binascii, textwrap, string

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aquí'  # Cambia esta cadena por una clave segura

# Diccionario global para almacenar las sesiones de juego (para propósitos demo)
games = {}

# Clase que contiene la lógica del juego adaptada para web (sin Tkinter)
class TerminalHackGameWeb:
    def __init__(self):
        self.current_stage = 0
        self.attempts = 3
        self.game_started = False
        self.secret_terminal_active = False
        self.spanish_mode = False
        self.command_translations = {}
        self.command_responses = {}
        self.output = []  # Acumula las líneas de salida que se enviarán al navegador
        self.game_over = False
        self.enigmas = []
        self.start_game()

    def append_output(self, text):
        self.output.append(text)

    def get_output(self):
        res = "\n".join(self.output)
        self.output = []
        return res

    def cesar_cipher(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                start = ord('a') if char.islower() else ord('A')
                result += chr((ord(char) - start + shift) % 26 + start)
            else:
                result += char
        return result

    def initialize_enigmas(self):
        if not self.spanish_mode:
            self.enigmas = [
                {
                    "type": "cesar",
                    "context": "ENCRYPTED TRANSMISSION FROM UNDERGROUND RESISTANCE",
                    "question": "Decrypt the message: {}",
                    "answer": "rojo",
                    "generator": lambda: self.cesar_cipher("rojo", 3),
                    "hint": "Caesar shift might reveal the truth..."
                },
                {
                    "type": "base64",
                    "context": "INTERCEPTED COMMUNICATION - BASE64 ENCODED",
                    "question": "Decode this transmission: {}",
                    "answer": "azul",
                    "generator": lambda: base64.b64encode("azul".encode()).decode(),
                    "hint": "Base64 is a common encoding method in covert communications"
                },
                {
                    "type": "hex",
                    "context": "CLASSIFIED DOCUMENT - HEX ENCODED",
                    "question": "Translate the hex code: {}",
                    "answer": "verde",
                    "generator": lambda: binascii.hexlify("verde".encode()).decode(),
                    "hint": "Hexadecimal is used in low-level system communications"
                },
                {
                    "type": "binary",
                    "context": "QUANTUM COMMUNICATION STREAM",
                    "question": "Decode the binary transmission: {}",
                    "answer": "amarillo",
                    "generator": lambda: ' '.join(format(ord(char), '08b') for char in "amarillo"),
                    "hint": "Binary is the fundamental language of computing"
                }
            ]
        # En modo español se asignarán los enigmas al activar el modo

    def start_game(self):
        self.secret_terminal_active = False
        self.game_started = False
        self.current_stage = 0
        self.attempts = 3
        self.game_over = False
        if not self.spanish_mode:
            self.initialize_enigmas()
            device_name = "WEB"
            welcome_text = f"""[SYSTEM INITIALIZE]
ENIGMA DECODER V2.1
SECURITY CLEARANCE: REQUIRED
LOGGED FROM: {device_name}

MISSION OBJECTIVE:
> Decrypt 4 classified transmissions
> Use decryption techniques to progress
> 3 ATTEMPTS PER TRANSMISSION

TYPE 'START' TO BEGIN MISSION - TYPE 'ESP' FOR SPANISH MODE
"""
        else:
            welcome_text = f"""[SISTEMA INICIALIZADO]
DECODIFICADOR ENIGMA V2.1
NIVEL DE SEGURIDAD: REQUERIDO
REGISTRADO DESDE: WEB

OBJETIVO DE LA MISIÓN:
> Descifrar 4 transmisiones clasificadas
> Usa técnicas de descifrado para avanzar
> 3 INTENTOS POR TRANSMISIÓN

ESCRIBE 'INICIAR' PARA COMENZAR LA MISIÓN
"""
        self.output = []
        self.append_output(welcome_text)

    def show_next_enigma(self):
        if self.current_stage < len(self.enigmas):
            enigma = self.enigmas[self.current_stage]
            context_text = f"\n[{enigma['context']}]\n"
            question_text = enigma['question'].format(enigma['generator']())
            self.append_output(context_text)
            self.append_output(question_text)
            self.append_output(f"HINT: {enigma['hint']}")
        else:
            self.complete_mission()

    def check_answer(self, user_answer):
        enigma = self.enigmas[self.current_stage]
        if user_answer.lower() == enigma['answer']:
            self.append_output("✓ TRANSMISSION SUCCESSFULLY DECODED" if not self.spanish_mode else "✓ TRANSMISIÓN DESCIFRADA CON ÉXITO")
            self.current_stage += 1
            self.attempts = 3
            if self.current_stage < len(self.enigmas):
                self.show_next_enigma()
            else:
                self.complete_mission()
        else:
            self.attempts -= 1
            if self.attempts > 0:
                self.append_output(f"✗ DECRYPTION FAILED. {self.attempts} ATTEMPTS REMAINING" if not self.spanish_mode else f"✗ DESCIFRADO FALLIDO. QUEDAN {self.attempts} INTENTOS")
            else:
                self.append_output("✗ MISSION FAILED." if not self.spanish_mode else "✗ MISIÓN FALLIDA.")
                self.mission_failed()

    def mission_failed(self):
        failure_text = """[CRITICAL SYSTEM FAILURE]
UNAUTHORIZED ACCESS DETECTED
TERMINAL SELF-DESTRUCTING IN 3... 2... 1..."""
        for i in range(3):
            self.append_output(failure_text)
        self.game_over = True

    def complete_mission(self):
        if not self.spanish_mode:
            success_text = """[MISSION COMPLETED]
ALL TRANSMISSIONS SUCCESSFULLY DECODED

SECURITY CLEARANCE: GRANTED
CONGRATULATIONS, AGENT!"""
        else:
            success_text = """[MISIÓN COMPLETADA]
TODAS LAS TRANSMISIONES FUERON DESCIFRADAS CON ÉXITO

AUTORIZACIÓN DE SEGURIDAD: CONCEDIDA
¡FELICIDADES, AGENTE!"""
        self.append_output(success_text)
        self.generate_intelligence_report()

    def generate_intelligence_report(self):
        if not self.spanish_mode:
            intel_report = """
-------------------------FOREIGN TRANSMISSION-----------------------------

[INTELLIGENCE REPORT - CODE: 'OPERATION REDLIGHT']

SUMMARY:
 A series of unauthorized transmissions were intercepted in recent weeks...
[Report truncated for brevity]"""
        else:
            intel_report = """
----------------------TRANSMISIÓN EXTRANJERA--------------------------

[INFORME DE INTELIGENCIA - CÓDIGO: 'OPERACIÓN LUZ ROJA']

RESUMEN:
 Se interceptaron una serie de transmisiones no autorizadas en las últimas semanas...
[Informe truncado por brevedad]"""
        self.append_output(intel_report)

    def activate_secret_terminal(self):
        device_name = "WEB"
        self.secret_terminal_active = True
        self.output = []  # Limpiamos la salida anterior
        self.append_output("[SECRET TERMINAL ACTIVATED]" if not self.spanish_mode else "[TERMINAL SECRETA ACTIVADA]")
        self.append_output(f"LOGGED FROM: {device_name.upper()}" if not self.spanish_mode else f"REGISTRADO DESDE: {device_name.upper()}")
        self.append_output("So... You are not satisfied" if not self.spanish_mode else "Así que... No estás satisfecho")
        self.append_output("This is just the beginning..." if not self.spanish_mode else "Esto es solo el comienzo...")
        self.append_output("A new mission awaits. You have been selected." if not self.spanish_mode else "Una nueva misión te espera. Has sido seleccionado.")
        self.append_output("Your skills are needed, more than ever." if not self.spanish_mode else "Tus habilidades son necesarias, más que nunca.")
        self.append_output("The path will be perilous, but you are not alone." if not self.spanish_mode else "El camino será peligroso, pero no estarás solo.")
        self.append_output("There will be challenges, secrets to uncover, and enemies to outwit." if not self.spanish_mode else "Habrá desafíos, secretos por descubrir y enemigos que superar.")
        self.append_output("Remember: The success of this mission depends on your choices." if not self.spanish_mode else "Recuerda: El éxito de esta misión depende de tus decisiones.")
        self.append_output("Prepare yourself. The first step is near." if not self.spanish_mode else "Prepárate. El primer paso está cerca.")
        self.append_output("END OF DEMO. THANKS FOR PLAYING - TYPE: 'EXIT'" if not self.spanish_mode else "FIN DE LA DEMO. GRACIAS POR JUGAR")

    def translate_ui_to_spanish(self):
        self.spanish_mode = True
        self.command_translations = {
            "simon": "simon",
            "ayuda": "help",
            "reiniciar": "reset",
            "cd": "cd",
            "limpiar": "clear",
            "salir": "exit",
            "ls": "ls",
            "directorio": "pwd",
            "quiensoy": "whoami",
            "manual": "man",
            "cat": "cat",
            "mkdir": "mkdir",
            "rm": "rm",
            "top": "top",
            "apagar": "shutdown",
            "señordelenigma": "lordofenigma",
            "iniciar": "start"
        }
        self.command_responses = {
            "help": "Pides AYUDA, pero estás solo, NADIE VENDRÁ",
            "reset": "REINICIANDO... pero ¿por qué? ¿Importa acaso?",
            "cd": "ERROR: Directorio no encontrado. Quizás nunca existió...",
            "clear": "La pantalla permanece sucia... ¿Qué intentas ocultar?",
            "exit": "Te dejaré ir... por ahora",
            "ls": "Listando... nada. No hay nada aquí.",
            "pwd": "¿Dónde estás? El camino se ha perdido. No hay directorio, solo vacío.",
            "whoami": "¿Quién eres? ¿Acaso importa en este punto...?",
            "man": "El manual está... vacío. Estás por tu cuenta.",
            "cat": "No hay nada que mostrar. No puedes leer lo que no existe.",
            "mkdir": "Directorio no creado... a lo sumo, todo es una ilusión.",
            "rm": "Crees que puedes borrar. No puedes borrar lo que ya se ha ido.",
            "top": "¿Top? No hay nada que monitorear. Excepto TÚ.",
            "shutdown": "Error al apagar... ¿pero con qué propósito? ¿Es esto realmente un final?"
        }
        self.enigmas = [
            {
                "type": "cesar",
                "context": "TRANSMISIÓN CIFRADA DE LA RESISTENCIA SUBTERRÁNEA",
                "question": "Descifra el mensaje: {}",
                "answer": "rojo",
                "generator": lambda: self.cesar_cipher("rojo", 3),
                "hint": "El cifrado César podría revelar la verdad..."
            },
            {
                "type": "base64",
                "context": "COMUNICACIÓN INTERCEPTADA - CODIFICADA EN BASE64",
                "question": "Decodifica esta transmisión: {}",
                "answer": "azul",
                "generator": lambda: base64.b64encode("azul".encode()).decode(),
                "hint": "Base64 es un método de codificación común en comunicaciones encubiertas"
            },
            {
                "type": "hex",
                "context": "DOCUMENTO CLASIFICADO - CODIFICADO EN HEXADECIMAL",
                "question": "Traduce el código hexadecimal: {}",
                "answer": "verde",
                "generator": lambda: binascii.hexlify("verde".encode()).decode(),
                "hint": "Hexadecimal se usa en comunicaciones de bajo nivel"
            },
            {
                "type": "binary",
                "context": "TRANSMISIÓN DE COMUNICACIÓN CUÁNTICA",
                "question": "Decodifica la transmisión binaria: {}",
                "answer": "amarillo",
                "generator": lambda: ' '.join(format(ord(char), '08b') for char in "amarillo"),
                "hint": "Binario es el lenguaje fundamental de la computación"
            }
        ]
        welcome_text = f"""[SISTEMA INICIALIZADO]
DECODIFICADOR ENIGMA V2.1
NIVEL DE SEGURIDAD: REQUERIDO
REGISTRADO DESDE: WEB

OBJETIVO DE LA MISIÓN:
> Descifrar 4 transmisiones clasificadas
> Usa técnicas de descifrado para avanzar
> 3 INTENTOS POR TRANSMISIÓN

ESCRIBE 'INICIAR' PARA COMENZAR LA MISIÓN
"""
        self.output = []
        self.append_output(welcome_text)

    def process_command(self, command):
        cmd = command.strip().lower()
        self.append_output(f"> {cmd}")
        # Si se escribe "esp", se activa el modo español
        if cmd == "esp":
            self.translate_ui_to_spanish()
            return self.get_output()
        # En modo español, si el juego aún no ha iniciado y el comando no está en el diccionario...
        if self.spanish_mode and not self.game_started and cmd not in self.command_translations:
            self.append_output("COMANDO INVÁLIDO. MODO ESPAÑOL ACTIVADO.")
            return self.get_output()
        # Se traduce el comando si corresponde
        translated_command = self.command_translations.get(cmd, cmd) if self.spanish_mode else cmd
        response = self.command_responses.get(translated_command, None)
        if translated_command == "simon":
            self.activate_secret_terminal()
        elif translated_command == "help":
            self.append_output(response if response else ("You call for HELP, but you are on your own, NOBODY CAME" if not self.spanish_mode else "Pides AYUDA, pero estás solo, NADIE VENDRÁ"))
        elif translated_command == "reset":
            self.append_output(response if response else ("RESETTING... but why? Does it even matter?" if not self.spanish_mode else "REINICIANDO... pero ¿por qué? ¿Importa acaso?"))
            self.start_game()
        elif translated_command == "cd":
            self.append_output(response if response else ("ERROR: Directory not found. Maybe it never existed..." if not self.spanish_mode else "ERROR: Directorio no encontrado. Quizás nunca existió..."))
        elif translated_command == "clear":
            self.append_output(response if response else ("The screen remains unclean... What are you trying to hide?" if not self.spanish_mode else "La pantalla permanece sucia... ¿Qué intentas ocultar?"))
        elif translated_command == "exit":
            self.append_output(response if response else ("I'll allow it, it's not too late..." if not self.spanish_mode else "Te dejaré ir... por ahora"))
            self.game_over = True
        elif translated_command == "ls":
            self.append_output(response if response else ("Listing... nothing. There's nothing here." if not self.spanish_mode else "Listando... nada. No hay nada aquí."))
        elif translated_command == "pwd":
            self.append_output(response if response else ("Where are you? The path is lost. There's no directory, only emptiness." if not self.spanish_mode else "¿Dónde estás? El camino se ha perdido. No hay directorio, solo vacío."))
        elif translated_command == "whoami":
            self.append_output(response if response else ("Who are you? Does it even matter at this point...?" if not self.spanish_mode else "¿Quién eres? ¿Acaso importa en este punto...?"))
        elif translated_command.startswith("man"):
            self.append_output(response if response else ("The manual is... empty. You are on your own." if not self.spanish_mode else "El manual está... vacío. Estás por tu cuenta."))
        elif translated_command.startswith("cat"):
            self.append_output(response if response else ("There's nothing to display. You can't read what's not there." if not self.spanish_mode else "No hay nada que mostrar. No puedes leer lo que no existe."))
        elif translated_command.startswith("mkdir"):
            self.append_output(response if response else ("Directory not created... at most it's all an illusion." if not self.spanish_mode else "Directorio no creado... a lo sumo, todo es una ilusión."))
        elif translated_command.startswith("rm"):
            self.append_output(response if response else ("You think you can delete? You can't erase what's already gone." if not self.spanish_mode else "Crees que puedes borrar. No puedes borrar lo que ya se ha ido."))
        elif translated_command.startswith("top"):
            self.append_output(response if response else ("Top? There's nothing to monitor. Except YOU." if not self.spanish_mode else "¿Top? No hay nada que monitorear. Excepto TÚ."))
        elif translated_command.startswith("synapse"):
            self.append_output("DONT. EVEN. TRY.")
            self.start_game()
        elif translated_command == "shutdown":
            self.append_output(response if response else ("Error Shutting down... but for what purpose? Is this really an end?" if not self.spanish_mode else "Error al apagar... ¿pero con qué propósito? ¿Es esto realmente un final?"))
        elif translated_command == "lordofenigma":
            self.complete_mission()
        elif translated_command == "start":
            self.game_started = True
            random.shuffle(self.enigmas)
            self.current_stage = 0
            self.attempts = 3
            self.show_next_enigma()
        elif self.game_started:
            self.check_answer(translated_command)
        else:
            self.append_output("INVALID COMMAND. TYPE 'START'." if not self.spanish_mode else "COMANDO INVÁLIDO. ESCRIBE 'INICIAR'.")
        return self.get_output()

# Función auxiliar para obtener (o crear) la sesión de juego según la sesión de Flask
def get_game():
    from flask import session
    if 'game_id' not in session:
        game_id = str(uuid.uuid4())
        session['game_id'] = game_id
        games[game_id] = TerminalHackGameWeb()
    else:
        game_id = session['game_id']
        if game_id not in games:
            games[game_id] = TerminalHackGameWeb()
    return games[game_id]

@app.route('/')
def index():
    game = get_game()
    # En la carga inicial se envía el mensaje de bienvenida
    output = game.get_output()
    return render_template('index.html', output=output)

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    user_command = data.get('command', '')
    game = get_game()
    if game.game_over:
        game.start_game()  # Reinicia el juego si terminó
    output = game.process_command(user_command)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
