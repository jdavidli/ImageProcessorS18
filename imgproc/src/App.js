import React from 'react'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import SimpleMenu from './upload.js'
import ClippedDrawer from './ClippedDrawer.js'
import axios from 'axios';

class App extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      filesDataFromChild: []
    }
  }

  myCallback = (files) => {
    this.setState({filesDataFromChild: files});
    console.log(files)
}

  render () {
    return (
      <div>
        <AppBar position='absolute'>
          <Toolbar>
            <Typography variant='title' color='inherit' style={{flex: 1}}>
            Image Processor
            </Typography>
            <SimpleMenu callbackFromParent={this.myCallback}/>
          </Toolbar>
        </AppBar>
        <ClippedDrawer />
      </div>
    )
  }
}

export default App
