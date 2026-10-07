import streamlit as st
from datetime import datetime, timedelta
import time
import streamlit.components.v1 as components


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Alarm Clock",
    page_icon="⏰",
    layout="centered"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e1b4b, #312e81);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.clock-box {
    background: rgba(255,255,255,0.10);
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    margin: 20px 0;
    border: 1px solid rgba(255,255,255,0.15);
}

.clock {
    font-size: 50px;
    font-weight: bold;
    color: #ffffff;
}

.status {
    text-align: center;
    font-size: 22px;
    padding: 15px;
    border-radius: 15px;
    background: rgba(255,255,255,0.10);
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "alarm_set" not in st.session_state:
    st.session_state.alarm_set = False

if "alarm_running" not in st.session_state:
    st.session_state.alarm_running = False

if "alarm_triggered" not in st.session_state:
    st.session_state.alarm_triggered = False


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">⏰ Smart Alarm Clock</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Set your alarm and never miss an important moment!'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CURRENT TIME
# =========================================================

now = datetime.now()

st.markdown(
    f"""
    <div class="clock-box">
        <div>🕐 Current Time</div>
        <div class="clock">{now.strftime("%I:%M:%S %p")}</div>
        <div>{now.strftime("%A, %d %B %Y")}</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ALARM TIME SELECTION
# =========================================================

st.subheader("🔔 Set Your Alarm")

default_alarm = (
    datetime.now() + timedelta(minutes=1)
).time().replace(second=0, microsecond=0)

alarm_time = st.time_input(
    "Choose Alarm Time",
    value=default_alarm
)


# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns(2)

with col1:
    start = st.button(
        "▶️ Start Alarm",
        use_container_width=True
    )

with col2:
    stop = st.button(
        "🛑 Stop Alarm",
        use_container_width=True
    )


# =========================================================
# START ALARM
# =========================================================

if start:

    st.session_state.alarm_set = True
    st.session_state.alarm_running = True
    st.session_state.alarm_triggered = False

    st.success(
        f"✅ Alarm set for {alarm_time.strftime('%I:%M %p')}"
    )


# =========================================================
# STOP ALARM
# =========================================================

if stop:

    st.session_state.alarm_set = False
    st.session_state.alarm_running = False
    st.session_state.alarm_triggered = False

    st.warning("🛑 Alarm stopped.")


# =========================================================
# ALARM RUNNING
# =========================================================

if st.session_state.alarm_running:

    current = datetime.now()

    alarm_datetime = datetime.combine(
        current.date(),
        alarm_time
    )

    # If today's alarm time has already passed,
    # schedule it for tomorrow.
    if alarm_datetime <= current:
        alarm_datetime += timedelta(days=1)

    remaining = alarm_datetime - current

    total_seconds = max(
        0,
        int(remaining.total_seconds())
    )

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    st.markdown(
        f"""
        <div class="status">
            ⏳ Alarm will ring in<br>
            <b>{hours:02d} : {minutes:02d} : {seconds:02d}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # ALARM TRIGGER
    # =====================================================

    if remaining.total_seconds() <= 1:

        st.session_state.alarm_running = False
        st.session_state.alarm_triggered = True

        st.error("🔔🔔 ALARM! WAKE UP! 🔔🔔")

        # Browser-based alarm sound.
        # This does NOT use winsound and works on Linux servers.
        components.html(
            """
            <script>
                function playAlarm() {

                    const AudioContext =
                        window.AudioContext ||
                        window.webkitAudioContext;

                    if (!AudioContext) {
                        return;
                    }

                    const audioContext = new AudioContext();

                    function beep(startTime, frequency) {

                        const oscillator =
                            audioContext.createOscillator();

                        const gain =
                            audioContext.createGain();

                        oscillator.type = "sine";
                        oscillator.frequency.value = frequency;

                        gain.gain.setValueAtTime(
                            0.0001,
                            startTime
                        );

                        gain.gain.exponentialRampToValueAtTime(
                            0.5,
                            startTime + 0.05
                        );

                        gain.gain.exponentialRampToValueAtTime(
                            0.0001,
                            startTime + 0.35
                        );

                        oscillator.connect(gain);
                        gain.connect(audioContext.destination);

                        oscillator.start(startTime);
                        oscillator.stop(startTime + 0.4);
                    }

                    const startTime =
                        audioContext.currentTime + 0.1;

                    for (let i = 0; i < 6; i++) {

                        beep(
                            startTime + (i * 0.6),
                            1000
                        );

                    }
                }

                playAlarm();
            </script>
            """,
            height=0
        )

        st.balloons()


# =========================================================
# ALARM STATUS
# =========================================================

if not st.session_state.alarm_running:

    if not st.session_state.alarm_set:

        if not st.session_state.alarm_triggered:

            st.markdown(
                '<div class="status">'
                '💤 No alarm is currently active'
                '</div>',
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        ⏰ Smart Alarm Clock • Built with Streamlit 🐍
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# REFRESH EVERY SECOND WHILE ALARM IS RUNNING
# =========================================================

if st.session_state.alarm_running:

    time.sleep(1)
    st.rerun()
