import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import Button from 'material-ui/Button'
import Menu, { MenuItem } from 'material-ui/Menu'
import SimpleMenu from './upload.js'
import ClippedDrawer from './ClippedDrawer.js'
import RecipeReviewCard from './previewcard.js'
import TitlebarGridList from './TitlebarGridList.js'
import TextField from 'material-ui/TextField';
import FileUpload from './File.js'

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
