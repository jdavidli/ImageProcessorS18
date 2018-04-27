import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import Drawer from 'material-ui/Drawer'
import { ListItem, ListItemText } from 'material-ui/List'
import TextField from 'material-ui/TextField'
import GridList, { GridListTile, GridListTileBar } from 'material-ui/GridList'
import IconButton from 'material-ui/IconButton'
import InfoIcon from '@material-ui/icons/Info'

const drawerWidth = 240
const styles = theme => ({
  root: {
    flexGrow: 1,
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex'
  },
  gridList: {
    width: 'auto'
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)'
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200
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
    this.state = {
      text: ''
    }
  }

  onCommand = (cmd) => {
    this.props.callbackFromCommand(cmd)
  }

onNameTextFieldChange = (event) => {
  this.setState({'text': event.target.value})
  this.props.callbackFromEmail(event)
}

render () {
  const { classes } = this.props
  const tileData = [
    {
      img: this.props.oImgParent
    },
    {
      img: this.props.pImgParent
    }
  ]
  return (
    <div className={classes.root}>
      <Drawer
        variant='permanent'
        classes={{
          paper: classes.drawerPaper
        }}
      >
        <div className={classes.toolbar} />
        <TextField id='email' label='Email' margin='normal' className={classes.textField}
          value={this.state.text} onChange={this.onNameTextFieldChange} />
        <ListItem button onClick={() => { this.onCommand(1) }}>
          <ListItemText primary='Histogram Equalization' />
        </ListItem>
        <ListItem button onClick={() => { this.onCommand(2) }}>
          <ListItemText primary='Contrast Stretching' />
        </ListItem>
        <ListItem button onClick={() => { this.onCommand(3) }}>
          <ListItemText primary='Log Compression' />
        </ListItem>
        <ListItem button onClick={() => { this.onCommand(4) }}>
          <ListItemText primary='Reverse Video' />
        </ListItem>
        <ListItem button onClick={() => { this.onCommand(5) }}>
          <ListItemText primary='Edge Detection' />
        </ListItem>
      </Drawer>
      <main className={classes.content}>
        <div className={classes.toolbar} />
          <GridList cellHeight={200} className={classes.gridList}>
            <GridListTile key='Subheader' cols={2} style={{ height: 'auto' }} />
            {tileData.map((tile,i) => (
              <GridListTile key={tile.img+i}>
                <img src={tile.img} />
                <GridListTileBar
                  actionIcon={
                    <IconButton className={classes.icon}>
                      <InfoIcon />
                    </IconButton>
                  }
                />
              </GridListTile>
            ))}
          </GridList>
      </main>
    </div>
  )
}
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(ClippedDrawer)
