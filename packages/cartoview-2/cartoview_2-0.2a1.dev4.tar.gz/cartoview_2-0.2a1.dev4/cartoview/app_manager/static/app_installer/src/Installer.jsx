import "@babel/polyfill/noConflict"
import 'semantic-ui-css/semantic.min.css'
import './css/installer.css'

import {
    Container,
    Grid,
    Message,
} from 'semantic-ui-react'
import React, { Component } from 'react'

import AppStoreSelector from './components/AppStoreSelector'
import AppsList from './components/AppsList'
import ErrorList from './components/ErrorList'
import { Provider } from 'react-redux'
import ReactDOM from 'react-dom'
import store from './store'

class AppInstaller extends Component {
    constructor(props) {
        super(props)
    }
    render() {
        return (
            <Provider store={store}>
                <div>
                    <Container id="main-container">
                        <Grid centered>
                            <Grid.Row centered>
                                <Grid.Column width={15}>
                                    <ErrorList />
                                </Grid.Column>
                            </Grid.Row>
                            <Grid.Row centered>
                                <Grid.Column width={15}>
                                    <Message warning>
                                        <Message.Header>{"Warning!"}</Message.Header>
                                        <p>{"Please note that the web server will be restarted after installing or uninstalling any application."}</p>
                                    </Message>
                                </Grid.Column>
                            </Grid.Row>
                            <Grid.Row centered>
                                <Grid.Column width={15}>
                                    <AppStoreSelector />
                                </Grid.Column>
                            </Grid.Row>
                            <Grid.Row>
                                <Grid.Column width={16}>
                                    <AppsList />
                                </Grid.Column>
                            </Grid.Row>
                        </Grid>
                    </Container>
                </div>
            </Provider>
        )
    }
}
var elem = document.getElementById("installer-app")
if (!elem) {
    elem = document.createElement('div', { "id": "installer-app" })
    document.body.appendChild(elem)
}
ReactDOM.render(<AppInstaller />, elem)
if (module.hot) {
    module.hot.accept()
}