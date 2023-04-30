start =
    🤖 <b>Добро пожаловать в ChatGPT!</b> 🚀

    Я - <i>умный и гибкий Телеграм-бот</i>, созданный для общения с вами в различных режимах чата.
    Вы сможете наслаждаться долгими и интересными беседами 🗨️🎉

    ✅ <b>Основные функции:</b>
    <code>1</code>. 🗨️🪬 Различные режимы чата:
        🔹🔮<i>стандартные</i>
        🔹🧠<i>продвинутые</i>
        🔹⚙️<i>кастомные</i>
    <code>2</code>. 💾 Сохранение всех ваших диалогов для возможности продолжить беседу в любой момент.
    <code>3</code>. ⚙️ Возможность изменить модель GPT в любое время.

    🚀 Чтобы начать, отправьте мне команду /start и затем выберите предпочитаемый вами режим чата!

    🔮 <b>Стандартные режимы</b> - это режимы, которые вы можете использовать сразу после запуска бота. Они включают в себя:
    <code>1</code>. <i>Обычный режим</i> - обычный режим чата с GPT-3.
    <code>2</code>. <i>Режим ролевой игры</i> - режим, в котором вы можете играть в ролевые игры с GPT-3.
    <code>3</code>. <i>Режим вопросов и ответов</i> - режим, в котором вы можете задавать вопросы GPT-3 и получать ответы.

    🧠 <b>Продвинутые режимы</b> - это режимы, которые вы можете разблокировать, отправив мне команду /unlock_advanced_modes. Они включают в себя:
    <code>1</code>. <i>Режим ролевой игры с персонажами</i> - режим, в котором вы можете играть в ролевые игры с персонажами GPT-3.

    ⚙️ <b>Кастомные режимы</b> - Создайте собственные кастомные режимы и получайте удовольствие от уникальных диалогов.

    🕐 Не забывайте, что вы всегда можете <b>продолжить свой диалог позже</b> - я сохраню всю историю ваших разговоров!

    🔧 Хотите изменить модель GPT? Просто напишите команду /change_model и выберите новую модель!

    🗨️ Приятного общения с <b>ChatGPT</b>! 🎉

model_changed =
    🔧 <b>Модель GPT изменена!</b> 🔧

    🤖 Текущая модель: <b>{$model}</b>

    🚀 Чтобы начать, отправьте мне команду /start и затем выберите предпочитаемый вами режим чата!

button-standard_modes = 🔮 Стандартные режимы
button-advanced_modes = 🧠 Продвинутые режимы
button-custom_modes = ⚙️ Кастомные режимы
button-dialogs = 🕐 Диалоги
button-skip = 〰️ Пропустить
button-back = « Назад

custom_modes =
    ⚙️ <b>Кастомные режимы</b> ⚙️

    📝 Создавайте свои собственные кастомные режимы чата, чтобы получать уникальный опыт общения с GPT!

    🗨️ Вам предоставляется возможность настроить и подстроить режимы под свои предпочтения и интересы.

    ✨ Наслаждайтесь общением в кастомных режимах!

    🗂 <b>Доступные кастомные режимы</b>:


custom_modes-button-create = 🆕 Создать новый кастомный режим
custom_mode =
    ⚙️ <b>Кастомный режим</b> ⚙️

    🏷 <b>Название:</b> {$name}

    📃 <b>Описание:</b> {$description}

    📥 <b>Промпт:</b> {$prompt}

custom_mode-button-start = 🚀 Начать новый диалог
custom_mode-button-edit = ✏️ Редактировать
custom_mode-button-update = 🔁 Обновить
custom_mode-button-delete = 🗑️ Удалить


custom_mode-create =
    🆕 <b>Создание нового кастомного режима</b> 🆕


    🏷 Введите <b>название</b>:

custom_mode-create-description =
    🆕 <b>Создание нового кастомного режима</b> 🆕

    🏷 <b>Название:</b> {$name}


    📃 Введите <b>описание</b>:

custom_mode-create-photo =
    🆕 <b>Создание нового кастомного режима</b> 🆕

    🏷 <b>Название:</b> {$name}

    📃 <b>Описание:</b> {$description}


    📷 <b>Фото:</b> прикрепите фото:

custom_mode-create-prompt =
    🆕 <b>Создание нового кастомного режима</b> 🆕

    🏷 <b>Название:</b> {$name}

    📃 <b>Описание:</b> {$description}


    📥 Введите <b>промпт</b>.

    Он будет использоваться для генерации ответов GPT.
    Примеры можете посмотреть в стандартных режимах.

custom_mode-create-success =
    🆕 <b>Создание нового кастомного режима</b> 🆕

    🏷 <b>Название:</b> {$name}

    📃 <b>Описание:</b> {$description}

    📥 <b>Промпт:</b> {$prompt}


    ✅ Кастомный режим успешно создан!


dialog-start =
    🚀 <b>Начало нового диалога</b> 🚀

    🏷 Введите <b>название</b>:


dialog-start-starting =
    🗨️ Диалог <code>{$name}</code> запущен!

    🔮 <b>Режим чата:</b> <code>{$mode}</code>

    🧠 <b>Текущая модель:</b> <code>{$model}</code>

dialog-continue_ =
    🕐 <b>Продолжение диалога</b>: <code>{$name}</code> 🕐

    🔮 <b>Режим чата:</b> <code>{$mode}</code>

    🧠 <b>Текущая модель:</b> <code>{$model}</code>


dialog-used_tokens =
    🔖 <b>Использовано токенов:</b> {$used_tokens}/{$max_tokens}

dialog-wait =
    ⏳ <b>Подождите...</b>

dialog-button-stop =
    🚫 Остановить диалог

dialog-stop =
    🛑 <b>Диалог остановлен.</b>

dialog-not_started=
    ❗️ <b>Диалог не запущен.</b>

dialog-no_dialogs =
    ❗️ Нет доступных диалогов по режиму <code>{$mode}</code>!

dialog-dialogs =
    🕐 <b>Диалоги</b> 🕐

    🔮 <b>Режим чата:</b> <code>{$mode}</code>

    🗨️ <b>Доступные диалоги:</b>

dialog-dialog =
    🕐 <b>Диалоги</b> 🕐

    🪬 <b>Режим чата:</b> <code>{$mode}</code>

    🧠 <b>Текущая модель:</b> <code>{$model}</code>



    📃 <b>Название:</b> <code>{$name}</code>

    🔖 <b>Использовано токенов:</b> {$used_tokens}/{$max_tokens}


dialog-button-continue_ = 🚀 Продолжить диалог
dialog-button-delete = 🗑️ Удалить диалог


dialog-delete-confirm =
    🗑️  Нажмите еще раз, чтобы подтвердить удаление.
dialog-deleted =
    🗑️ Диалог <code>{$name}</code> удален.