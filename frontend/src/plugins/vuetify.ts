// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles/main.css'

import {createVuetify, ThemeDefinition} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import theme from '../settings/colourTheme.json'

const myCustomTheme: ThemeDefinition = {
    dark: false,
    colors: theme
}

export const vuetify = createVuetify({
    theme: {
        defaultTheme: 'myCustomTheme',
        themes: {
            myCustomTheme,
        },
    },
    components,
    directives,
})