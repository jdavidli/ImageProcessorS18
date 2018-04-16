import React, { Component } from 'react'
import logo from './logo.svg'
import './App.css'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'

class App extends Component {
  render () {
    return (
      <div>
        <AppBar position='static' color='default'>
          <Toolbar>
            <Typography variant='title' color='inherit'>
              Image Processor
            </Typography>
          </Toolbar>
        </AppBar>
      </div>
    )
  }
}

export default App
