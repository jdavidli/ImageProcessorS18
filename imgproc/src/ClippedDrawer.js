import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import Drawer from 'material-ui/Drawer'
import List, { ListItem, ListItemText } from 'material-ui/List'
import TitlebarGridList from './TitlebarGridList.js'

class ClippedDrawer extends React.Component {
  render () {
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
        minWidth: 0 // So the Typography noWrap works
      },
      toolbar: theme.mixins.toolbar
    })

    return (
      <div>
        <Drawer variant='permanent'>
          <div />
          <ListItem button>
            <ListItemText primary='Histogram Equalization' />
          </ListItem>
          <ListItem button>
            <ListItemText primary='Contrast Stretching' />
          </ListItem>
          <ListItem button>
            <ListItemText primary='Log Compression' />
          </ListItem>
          <ListItem button>
            <ListItemText primary='Reverse Video' />
          </ListItem>
        </Drawer>
        <main>
          <div />
          <TitlebarGridList />
        </main>
      </div>
    )
  }
}

export default ClippedDrawer
