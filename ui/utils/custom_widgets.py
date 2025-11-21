import streamlit as st

def slider_with_number_input(label: str,
                             value: float,
                             key: str,
                             min_value: float= - 1e53 + 1,
                             max_value: float=   1e53 - 1,
                             step: float=0.01):
    widget = SliderNumberInput(label=label, value=value, key=key, min_value=min_value, max_value=max_value, step=step)
    value = widget.create_widget()
    return value

class SliderNumberInput:
    def __init__(self,
                label: str,
                value: float,
                key: str,
                min_value: float= - 1e53 + 1,
                max_value: float=   1e53 - 1,
                step: float=0.01):
        self.label = label
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.key = key


    def create_widget(self):
        self.value = st.slider(self.label, min_value=self.min_value, max_value=self.max_value, value=self.value, key=f'{self.key}_slider', on_change=self.update_num_input)
        self.value = st.number_input(self.label, min_value=self.min_value, value=self.value, step=self.step, label_visibility="collapsed", on_change=self.update_slider, key=f'{self.key}_num_input')
        return self.value

    def update_slider(self):
        st.session_state[f'{self.key}_slider'] = st.session_state[f'{self.key}_num_input']

    def update_num_input(self):
        st.session_state[f'{self.key}_num_input'] = st.session_state[f'{self.key}_slider']
