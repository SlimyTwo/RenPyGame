/*
    AHK KEYS CHEATSHEET / LEDGER
    =============================

    -- Mouse --
    LButton         ; Primary mouse button (usually left)
    RButton         ; Secondary mouse button (usually right)
    MButton         ; Middle button (or wheel button)

    -- Advanced Mouse Buttons --
    XButton1        ; Fourth mouse button (typically Browser_Back)
    XButton2        ; Fifth mouse button (typically Browser_Forward)

    -- Mouse Wheel --
    WheelUp         ; Wheel turned upward (away from you)
    WheelDown       ; Wheel turned downward (toward you)
    WheelLeft       ; Wheel tilt or secondary wheel scrolling left
    WheelRight      ; Wheel tilt or secondary wheel scrolling right
    ; (Note: Not all mice support lateral wheel events.)

    -- Keyboard (General Keys) --
    CapsLock        ; Caps Lock key (see “CapsLock and IME” below)
    Space           ; Space bar
    Tab             ; Tab key
    Enter           ; Enter (Return) key
    Escape (Esc)    ; Escape key
    Backspace (BS)  ; Backspace key

    -- Cursor Control Keys --
    ScrollLock      ; Scroll Lock key (Ctrl+ScrollLock may produce CtrlBreak)
    Delete (Del)    ; Delete key
    Insert (Ins)    ; Insert key
    Home            ; Home key
    End             ; End key
    PgUp            ; Page Up key
    PgDn            ; Page Down key
    Up              ; Up arrow
    Down            ; Down arrow
    Left            ; Left arrow
    Right           ; Right arrow

    -- Numpad Keys --
    Numpad0 / NumpadIns   ; 0 (or Ins) on the numeric keypad
    Numpad1 / NumpadEnd   ; 1 (or End)
    Numpad2 / NumpadDown  ; 2 (or Down arrow)
    Numpad3 / NumpadPgDn  ; 3 (or Page Down)
    Numpad4 / NumpadLeft  ; 4 (or Left arrow)
    Numpad5 / NumpadClear ; 5 (or Clear – usually does nothing)
    Numpad6 / NumpadRight ; 6 (or Right arrow)
    Numpad7 / NumpadHome  ; 7 (or Home)
    Numpad8 / NumpadUp    ; 8 (or Up arrow)
    Numpad9 / NumpadPgUp  ; 9 (or Page Up)
    NumpadDot / NumpadDel ; Decimal point / Delete key
    NumLock         ; Num Lock key (use ^Pause in hotkeys for Pause when Ctrl is held)

    ; Numpad arithmetic keys:
    NumpadDiv       ; Numpad Division key (/)
    NumpadMult      ; Numpad Multiplication key (*)
    NumpadAdd       ; Numpad Addition key (+)
    NumpadSub       ; Numpad Subtraction key (-)
    NumpadEnter     ; Numpad Enter key

    -- Function Keys --
    F1  - F24      ; Function keys (12 or more, depending on your keyboard)

    -- Modifier Keys --
    LWin            ; Left Windows key; can be referenced as <#
    RWin            ; Right Windows key; can be referenced as >#
    Control (Ctrl)  ; Control key; hotkey prefix: ^
    Alt             ; Alt key; prefix: !
    Shift           ; Shift key; prefix: +
    LControl (LCtrl); Left Control; prefix: <^
    RControl (RCtrl); Right Control; prefix: >^
    LShift          ; Left Shift; prefix: <+
    RShift          ; Right Shift; prefix: >+
    LAlt            ; Left Alt; prefix: <!
    RAlt            ; Right Alt; prefix: >!
    ; Note: For keyboards with AltGr, use <^>! to reference AltGr.

    -- Multimedia Keys --
    Browser_Back      ; Typically goes to “Back”
    Browser_Forward   ; Typically “Forward”
    Browser_Refresh   ; Refresh page
    Browser_Stop      ; Stop page load
    Browser_Search    ; Search
    Browser_Favorites ; Favorites
    Browser_Home      ; Homepage
    Volume_Mute       ; Mute volume
    Volume_Down       ; Lower volume
    Volume_Up         ; Increase volume
    Media_Next        ; Next media track
    Media_Prev        ; Previous media track
    Media_Stop        ; Stop media playback
    Media_Play_Pause  ; Toggle play/pause
    Launch_Mail       ; Launch default email client
    Launch_Media      ; Launch default media player
    Launch_App1       ; Launch “This PC” (or My Computer)
    Launch_App2       ; Launch Calculator

    -- Other Keys --
    AppsKey         ; Menu key (opens context menu)
    PrintScreen     ; Print Screen key
    CtrlBreak       ; Ctrl + Pause/Break or Ctrl+ScrollLock combination
    Pause           ; Pause key (use ^CtrlBreak in hotkeys if needed)
    Help            ; Help key (if available)
    Sleep           ; Sleep key (if supported)
    ; For any “mystery key” not shown in the list, use its Scan Code (SCnnn) or Virtual Key (VKnn)

    -- Game Controller (Gamepad, Joystick, etc.) --
    ; Buttons: Joy1 through Joy32
    ; Axes: JoyX (horizontal), JoyY (vertical), JoyZ (depth/altitude)
    ; Other controls: JoyR (rudder), JoyU, JoyV, and POV (Hat) controls.
    ; To reference a specific controller beyond the first, prefix with its number, e.g. 2Joy1

    -- Special Keys --
    ; SCnnn and VKnn may be used to reference keys by their scan or virtual key codes.
    ; For keys that aren’t directly recognized or for low-level remapping.
    ; Example: SC159:: ; defines a hotkey using scan code 159.
    ; Example: {vkFFsc159} sends a key with Virtual Key FF and scan code 159.

    ----------------------------------------------------------------------------
    Reference:
    This cheatsheet is based on the "List of Keys (Keyboard, Mouse and Controller)" page from the AutoHotkey documentation.
    (See :contentReference[oaicite:0]{index=0} for the AutoHotkey v2 remapping documentation and related details.)
*/

#Requires AutoHotkey v2.0

; Bind Alt + E to Up Arrow
!e:: {
    Send("{Up}")  ; Sends the Up Arrow key
}

; Bind Alt & S to Left Arrow
!s:: {
    Send("{Left}")  ; Sends the Left Arrow key
}

; Bind Alt & D to Down Arrow
!d:: {
    Send("{Down}")  ; Sends the Down Arrow key
}

; Bind Alt & F to Right Arrow
!f:: {
    Send("{Right}")  ; Sends the Right Arrow key
}

;*******************************************
;** Allows for highlighting with E S F D  **
;*******************************************

!+e:: {
    Send("+{Up}")
}

!+s:: {
    Send("+{Left}")
}

!+d:: {
    Send("+{Down}")
}

!+f:: {
    Send("+{Right}")
}

;*******************************************
;** Allows for ctrl jumping with E S F D  **
;*******************************************

!^e:: {
    Send("^{Up}")
}

!^s:: {
    Send("^{Left}")
}

!^d:: {
    Send("^{Down}")
}

!^f:: {
    Send("^{Right}")
}

;*******************************************
;** Allows ctrl jump & highlight for ESFD **
;*******************************************

!^+e:: {
    Send("^+{Up}")
}

!^+s:: {
    Send("^+{Left}")
}

!^+d:: {
    Send("^+{Down}")
}

!^+f:: {
    Send("^+{Right}")
}

;*******************************************

; Binds Alt a to home
!a:: {
    Send("{Home}")
}

; Binds Alt g to end
!g:: {
    Send("{End}")
}

;*******************************************
;** Allows ctrl jumping with Home & End   **
;*******************************************

!^a:: {
    Send("^{Home}")
}

!^g:: {
    Send("^{End}")
}

;*******************************************
;** Allows highlighting with Home & End   **
;*******************************************
!+a:: {
    Send("+{Home}")
}

!+g:: {
    Send("+{End}")
}

;*******************************************
;****        IntelliJ Shortcuts         ****
;*******************************************

; Expands Selection
!q:: {
    Send("^{w}")
}

; Moves Line Up
!w:: {
    Send("!+{Up}")
}

; Moves Line Down
!r:: {
    Send("!+{Down}")
}

; Binds f2 to the refactor shortcut
f2:: {
    Send("+{f6}")
}

; Binds alt+j to left mouse click
!j:: {
    Send("{LButton}")
}

; Binds alt+k to right mouse click
!k:: {
    Send("{RButton}")
}

; Binds alt+ctrl+j to ctrl mouse click
!^j:: {
    Send("^{b}")
}

; Binds alt+m to close window tab
!m:: {
    Send("^{F4}")
}

; Collapses Block
!;:: {
    Send("^{NumpadAdd}")
}

; Expands Block
!l:: {
    Send("^{NumpadSub}")
}

; Collapses Main Block
!+;:: {
    Send("^+{NumpadAdd}")
}

; Expands Main Block
!+l:: {
    Send("^+{NumpadSub}")
}

; Pressing P sends user to jetbrains keyboard shortcut documentation
!p:: {
    Run("https://www.jetbrains.com/help/idea/reference-keymap-win-default.html#basic_editing")
}

; Runs Program in IntelliJ
^Enter:: {
    Send("+{F10}")
}
