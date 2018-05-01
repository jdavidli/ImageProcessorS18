import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import Drawer from 'material-ui/Drawer'
import { ListItem, ListItemText } from 'material-ui/List'
import TextField from 'material-ui/TextField'
import GridList, { GridListTile, GridListTileBar } from 'material-ui/GridList'
import IconButton from 'material-ui/IconButton'
import InfoIcon from '@material-ui/icons/Info'
import Dialog, { DialogTitle, DialogContent, DialogContentText} from 'material-ui/Dialog'
import {AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip} from 'recharts'

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
      text: '',
      open: false
    }
  }

  onCommand = (cmd) => {
    this.props.callbackFromCommand(cmd)
  }

onNameTextFieldChange = (event) => {
  this.setState({'text': event.target.value})
  this.props.callbackFromEmail(event)
}

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };



render () {
  const { classes } = this.props
  const tileData = [
    {
      img: this.props.oImgParent,
      uptime: this.props.uTime,
      proctime: this.props.pTime,
      upsize: this.props.uSize
    },
    {
      img: this.props.pImgParent,
      uptime: this.props.uTime,
      proctime: this.props.pTime,
      upsize: this.props.uSize
    }
  ]

  // graphing
  const preOData = this.props.oHist[0]
  const lgProps = [{ dataKey: 'R', values: preOData}]
  console.log(lgProps)
  var oData = []
  var oJSON = {}
  for (var i in preOData) {
    oData.push({"R": preOData[i]})
  }
  console.log(oData)

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
          {tileData.map((tile, i) => (
            <GridListTile key={tile.img + i}>
              <img src={tile.img} />
              <GridListTileBar
                actionIcon={
                  <IconButton className={classes.icon} onClick={this.handleClickOpen}>
                  <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Image Information"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
            <AreaChart width={600} height={400} data={oData}
                  margin={{top: 10, right: 30, left: 0, bottom: 0}}>
              <CartesianGrid strokeDasharray="3 3"/>
              <XAxis dataKey="name"/>
              <YAxis/>
              <Area type='monotone' dataKey='R' stackId="1" stroke='#8884d8' fill='#8884d8' />
            </AreaChart>
              Uploaded time: {tile.uptime}
              <br/>
              Processing time: {tile.proctime}
              <br/>
              Image size: {tile.upsize}
            </DialogContentText>
          </DialogContent>
        </Dialog>
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
