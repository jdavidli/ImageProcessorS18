import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import GridList, { GridListTile, GridListTileBar } from 'material-ui/GridList'
import IconButton from 'material-ui/IconButton'
import InfoIcon from '@material-ui/icons/Info'
import Dialog, { DialogTitle, DialogContent, DialogContentText} from 'material-ui/Dialog'
import {AreaChart, Area, XAxis, YAxis} from 'recharts'
import SimpleDialog from './SimpleDialog.js'

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper
  },
  gridList: {
    width: 500
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)'
  }
})

class TitlebarGridList extends React.Component {
  constructor (props) {
    super()
    this.props = props
    this.state = {
      open: false,
      open2: false
    }
  }



  handleClickOpen = () => {
    this.setState({open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  handleClickOpen2 = () => {
    this.setState({ open2: true })
  };

  handleClose2 = () => {
    this.setState({ open2: false })
  };

  render () {
    const { classes } = this.props
    const origTileData = this.props.oTile

    const procTileData = this.props.pTile

    return (
      <div className={classes.root}>
        <GridList cellHeight={200} className={classes.gridList}>
          <GridListTile key='Subheader' cols={1} style={{ height: 'auto' }} />
          {origTileData.map((tile, i) => (
            <GridListTile key={tile.img + i}>
              <img src={tile.img} />
              <GridListTileBar
                actionIcon={
                  <IconButton className={classes.icon} onClick={this.handleClickOpen}>
                    <SimpleDialog open={this.state.open} onClose={this.handleClose}/>
                    <InfoIcon />
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>

        <GridList cellHeight={200} className={classes.gridList}>
          <GridListTile key='Subheader2' cols={1} style={{ height: 'auto' }} />
          {procTileData.map((tile, j) => (
            <GridListTile key={tile.img + j}>
              <img src={tile.img} />
              <GridListTileBar
                actionIcon={
                  <IconButton className={classes.icon} onClick={this.handleClickOpen2}>
                    <Dialog
                      open={this.state.open2}
                      onClose={this.handleClose2}
                      aria-labelledby='alert-dialog-title2'
                      aria-describedby='alert-dialog-description2'
                    >
                      <DialogTitle id='alert-dialog-title2'>{'Processed Image Information'}</DialogTitle>
                      <DialogContent>
                        <DialogContentText id='alert-dialog-description2'>

            Processing time: {tile.proctime}
                          <br />
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
      </div>
    )
  }
}

TitlebarGridList.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(TitlebarGridList)
