import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import SimpleMenu from './upload.js'
import ClippedDrawer from './ClippedDrawer.js'

const styles = {
  root: {
    flexGrow: 1
  },
  flex: {
    flex: 1
  }
}


function ButtonAppBar (props) {
  const { classes } = props
  return (
    <div className={classes.root}>
      <AppBar position='absolute'>
        <Toolbar>
          <Typography variant='title' color='inherit' className={classes.flex}>
            Image Processor
          </Typography>
          <SimpleMenu>
          </SimpleMenu>
        </Toolbar>
      </AppBar>
      <ClippedDrawer>
      </ClippedDrawer>
    </div>
  )
}

ButtonAppBar.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(ButtonAppBar)
