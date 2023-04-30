from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    button: Button
    custom_modes: Custom_modes
    custom_mode: Custom_mode
    dialog: Dialog

    @staticmethod
    def start() -> Literal["""🤖 &lt;b&gt;Добро пожаловать в ChatGPT!&lt;/b&gt; 🚀

Я - &lt;i&gt;умный и гибкий Телеграм-бот&lt;/i&gt;, созданный для общения с вами в различных режимах чата.
Вы сможете наслаждаться долгими и интересными беседами 🗨️🎉

✅ &lt;b&gt;Основные функции:&lt;/b&gt;
&lt;code&gt;1&lt;/code&gt;. 🗨️ Различные режимы чата:
    🔹🔮&lt;i&gt;стандартные&lt;/i&gt;
    🔹🧠&lt;i&gt;продвинутые&lt;/i&gt;
    🔹⚙️&lt;i&gt;кастомные&lt;/i&gt;
&lt;code&gt;2&lt;/code&gt;. 💾 Сохранение всех ваших диалогов для возможности продолжить беседу в любой момент.
&lt;code&gt;3&lt;/code&gt;. ⚙️ Возможность изменить модель GPT в любое время.

🚀 Чтобы начать, отправьте мне команду /start и затем выберите предпочитаемый вами режим чата!

🔮 &lt;b&gt;Стандартные режимы&lt;/b&gt; - это режимы, которые вы можете использовать сразу после запуска бота. Они включают в себя:
&lt;code&gt;1&lt;/code&gt;. &lt;i&gt;Обычный режим&lt;/i&gt; - обычный режим чата с GPT-3.
&lt;code&gt;2&lt;/code&gt;. &lt;i&gt;Режим ролевой игры&lt;/i&gt; - режим, в котором вы можете играть в ролевые игры с GPT-3.
&lt;code&gt;3&lt;/code&gt;. &lt;i&gt;Режим вопросов и ответов&lt;/i&gt; - режим, в котором вы можете задавать вопросы GPT-3 и получать ответы.

🧠 &lt;b&gt;Продвинутые режимы&lt;/b&gt; - это режимы, которые вы можете разблокировать, отправив мне команду /unlock_advanced_modes. Они включают в себя:
&lt;code&gt;1&lt;/code&gt;. &lt;i&gt;Режим ролевой игры с персонажами&lt;/i&gt; - режим, в котором вы можете играть в ролевые игры с персонажами GPT-3.

⚙️ &lt;b&gt;Кастомные режимы&lt;/b&gt; - Создайте собственные кастомные режимы и получайте удовольствие от уникальных диалогов.

🕐 Не забывайте, что вы всегда можете &lt;b&gt;продолжить свой диалог позже&lt;/b&gt; - я сохраню всю историю ваших разговоров!

🔧 Хотите изменить модель GPT? Просто напишите команду /change_model и выберите новую модель!

🗨️ Приятного общения с &lt;b&gt;ChatGPT&lt;/b&gt;! 🎉"""]: ...

    @staticmethod
    def model_changed(*, model) -> Literal["""🔧 &lt;b&gt;Модель GPT изменена!&lt;/b&gt; 🔧

🤖 Текущая модель: &lt;b&gt;{ $model }&lt;/b&gt;

🚀 Чтобы начать, отправьте мне команду /start и затем выберите предпочитаемый вами режим чата!"""]: ...


class Button:
    @staticmethod
    def standard_modes() -> Literal["""🔮 Стандартные режимы"""]: ...

    @staticmethod
    def advanced_modes() -> Literal["""🧠 Продвинутые режимы"""]: ...

    @staticmethod
    def custom_modes() -> Literal["""⚙️ Кастомные режимы"""]: ...

    @staticmethod
    def dialogs() -> Literal["""🕐 Мои диалоги"""]: ...

    @staticmethod
    def skip() -> Literal["""〰️ Пропустить"""]: ...

    @staticmethod
    def back() -> Literal["""« Назад"""]: ...


class Custom_modes:
    button: Custom_modesButton

    @staticmethod
    def __call__() -> Literal["""⚙️ &lt;b&gt;Кастомные режимы&lt;/b&gt; ⚙️

📝 Создавайте свои собственные кастомные режимы чата, чтобы получать уникальный опыт общения с GPT!

🗨️ Вам предоставляется возможность настроить и подстроить режимы под свои предпочтения и интересы.

✨ Наслаждайтесь общением в кастомных режимах!

🗂 &lt;b&gt;Доступные кастомные режимы&lt;/b&gt;:"""]: ...


class Custom_modesButton:
    @staticmethod
    def create() -> Literal["""🆕 Создать новый кастомный режим"""]: ...


class Custom_mode:
    button: Custom_modeButton
    create: Custom_modeCreate

    @staticmethod
    def __call__(*, name, description, prompt) -> Literal["""⚙️ &lt;b&gt;Кастомный режим&lt;/b&gt; ⚙️

🏷 &lt;b&gt;Название:&lt;/b&gt; { $name }
📃 &lt;b&gt;Описание:&lt;/b&gt; { $description }
📥 &lt;b&gt;Промпт:&lt;/b&gt; { $prompt }"""]: ...


class Custom_modeButton:
    @staticmethod
    def start() -> Literal["""🚀 Начать новый диалог"""]: ...

    @staticmethod
    def edit() -> Literal["""✏️ Редактировать"""]: ...

    @staticmethod
    def update() -> Literal["""🔁 Обновить"""]: ...

    @staticmethod
    def delete() -> Literal["""🗑️ Удалить"""]: ...


class Custom_modeCreate:
    @staticmethod
    def __call__() -> Literal["""🆕 &lt;b&gt;Создание нового кастомного режима&lt;/b&gt; 🆕

🏷 Введите &lt;b&gt;название&lt;/b&gt;:"""]: ...

    @staticmethod
    def description(*, name) -> Literal["""🆕 &lt;b&gt;Создание нового кастомного режима&lt;/b&gt; 🆕

🏷 &lt;b&gt;Название:&lt;/b&gt; { $name }
📃 Введите &lt;b&gt;описание&lt;/b&gt;:"""]: ...

    @staticmethod
    def photo(*, name, description) -> Literal["""🆕 &lt;b&gt;Создание нового кастомного режима&lt;/b&gt; 🆕

🏷 &lt;b&gt;Название:&lt;/b&gt; { $name }
📃 &lt;b&gt;Описание:&lt;/b&gt; { $description }
📷 &lt;b&gt;Фото:&lt;/b&gt; прикрепите фото:"""]: ...

    @staticmethod
    def prompt(*, name, description) -> Literal["""🆕 &lt;b&gt;Создание нового кастомного режима&lt;/b&gt; 🆕

🏷 &lt;b&gt;Название:&lt;/b&gt; { $name }
📃 &lt;b&gt;Описание:&lt;/b&gt; { $description }
📥 Введите &lt;b&gt;промпт&lt;/b&gt;.
Он будет использоваться для генерации ответов GPT.
Примеры можете посмотреть в стандартных режимах."""]: ...

    @staticmethod
    def success(*, name, description, prompt) -> Literal["""🆕 &lt;b&gt;Создание нового кастомного режима&lt;/b&gt; 🆕

🏷 &lt;b&gt;Название:&lt;/b&gt; { $name }
📃 &lt;b&gt;Описание:&lt;/b&gt; { $description }
📥 &lt;b&gt;Промпт:&lt;/b&gt; { $prompt }

✅ Кастомный режим успешно создан!"""]: ...


class Dialog:
    start: DialogStart
    button: DialogButton

    @staticmethod
    def used_tokens(*, used_tokens, max_tokens) -> Literal["""🔖 &lt;b&gt;Использовано токенов:&lt;/b&gt; { $used_tokens }/{ $max_tokens }"""]: ...

    @staticmethod
    def wait() -> Literal["""⏳ &lt;b&gt;Подождите...&lt;/b&gt;"""]: ...

    @staticmethod
    def stop() -> Literal["""🛑 &lt;b&gt;Диалог остановлен.&lt;/b&gt;"""]: ...

    @staticmethod
    def not_started() -> Literal["""❗️ &lt;b&gt;Диалог не запущен.&lt;/b&gt;"""]: ...


class DialogStart:
    @staticmethod
    def __call__() -> Literal["""🚀 &lt;b&gt;Начало нового диалога&lt;/b&gt; 🚀

🏷 Введите &lt;b&gt;название&lt;/b&gt;:"""]: ...

    @staticmethod
    def starting(*, model) -> Literal["""🗨️ &lt;b&gt;Диалог запущен.&lt;/b&gt;

🧠 &lt;b&gt;Текущая модель:&lt;/b&gt; &lt;code&gt;{ $model }&lt;/code&gt;"""]: ...


class DialogButton:
    @staticmethod
    def stop() -> Literal["""🚫 Остановить диалог"""]: ...

