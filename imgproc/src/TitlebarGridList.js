import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import GridList, { GridListTile, GridListTileBar } from 'material-ui/GridList'
import IconButton from 'material-ui/IconButton'
import InfoIcon from '@material-ui/icons/Info'
import Dialog, { DialogTitle, DialogContent, DialogContentText} from 'material-ui/Dialog'
import {AreaChart, Area, XAxis, YAxis} from 'recharts'
import SimpleDialog from './SimpleDialog.js'
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';

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
      open2: false,
      tile: null
    }
  }

passItemToModal = (item) => {
  this.setState({tile: item})
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
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Original Image</TableCell>
            <TableCell>Upload Time</TableCell>
            <TableCell>Image Size</TableCell>
            <TableCell>Original Histogram </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {origTileData.map(n => {
            return (
              <TableRow>
                <TableCell><img src={n.img} /></TableCell>
                <TableCell>{n.uptime}</TableCell>
                <TableCell>{n.upsize}</TableCell>
                <TableCell>{<AreaChart width={550} height={400} data={n.oHist}
                  margin={{top: 10, right: 10, left: 0, bottom: 0}}>
                  <XAxis ticks={[0, 255]} />
                  <YAxis />
                  <Area type='monotone' dataKey='R' stackId='1' stroke='#8884d8' fill='#8884d8' />
                </AreaChart>}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Processed Image</TableCell>
            <TableCell>Processing Time</TableCell>
            <TableCell>Image Size</TableCell>
            <TableCell>Processed Histogram </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {procTileData.map(m => {
            return (
              <TableRow>
                <TableCell><img src={m.img} /></TableCell>
                <TableCell>{m.proctime}</TableCell>
                <TableCell>{m.upsize}</TableCell>
                <TableCell>{<AreaChart width={550} height={400} data={m.pHist}
                  margin={{top: 10, right: 10, left: 0, bottom: 0}}>
                  <XAxis ticks={[0, 255]} />
                  <YAxis />
                  <Area type='monotone' dataKey='R' stackId='1' stroke='#8884d8' fill='#8884d8' />
                </AreaChart>}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>

        <GridList cellHeight={200} className={classes.gridList} >
          <GridListTile key='Subheader' cols={1} style={{ height: 'auto' }} />
          {origTileData.map((tile, i) => (
            <GridListTile key={tile.img + i}>
              <img src={tile.img} />
              <GridListTileBar
                actionIcon={
                  <IconButton className={classes.icon} onClick={this.handleClickOpen} >
                    <SimpleDialog open={this.state.open} onClose={this.handleClose} tile={this.state.tile}/>
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
