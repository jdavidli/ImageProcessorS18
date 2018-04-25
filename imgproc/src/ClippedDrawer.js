import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import Drawer from 'material-ui/Drawer'
import { ListItem, ListItemText } from 'material-ui/List'
import TitlebarGridList from './TitlebarGridList.js'

const drawerWidth = 240
const styles = theme => ({
  root: {
    flexGrow: 1,
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex'
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1
  },
  drawerPaper: {
    position: 'relative',
    width: drawerWidth
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    minWidth: 0
  },
  toolbar: theme.mixins.toolbar
})

class ClippedDrawer extends React.Component {
  constructor (props) {
    super()
    this.props = props
  }

  onCommand = (cmd) => {
    this.props.callbackFromCommand(cmd)
  }

  render () {
    const { classes } = this.props

    return (
      <div className={classes.root}>
        <Drawer
          variant='permanent'
          classes={{
            paper: classes.drawerPaper
          }}
        >
          <div className={classes.toolbar} />
          <ListItem button onClick={() => { this.onCommand(1)}}>
            <ListItemText primary='Histogram Equalization' />
          </ListItem>
          <ListItem button onClick={() => { this.onCommand(2)}}>
            <ListItemText primary='Contrast Stretching' />
          </ListItem>
          <ListItem button onClick={() => { this.onCommand(3)}}>
            <ListItemText primary='Log Compression' />
          </ListItem>
          <ListItem button onClick={() => { this.onCommand(4)}}>
            <ListItemText primary='Reverse Video' />
          </ListItem>
          <ListItem button onClick={() => { this.onCommand(5)}}>
            <ListItemText primary='Edge Detection' />
          </ListItem>
        </Drawer>
        <main className={classes.content}>
          <div className={classes.toolbar} />
          <TitlebarGridList />
        </main>
      </div>
    )
  }
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(ClippedDrawer)
