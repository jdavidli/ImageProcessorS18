import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Typography from 'material-ui/Typography';
import Divider from 'material-ui/Divider'
import TitlebarGridList from './TitlebarGridList.js'

const drawerWidth = 240;

const styles = theme => ({
  root: {
    flexGrow: 1,
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawerPaper: {
    position: 'relative',
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    minWidth: 0, // So the Typography noWrap works
  },
  toolbar: theme.mixins.toolbar,
});

function ClippedDrawer(props) {
  const { classes } = props;

  return (
    <div className={classes.root}>
      <Drawer
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <div className={classes.toolbar} />
        <ListItem button>
          <ListItemText primary="Histogram Equalization" />
        </ListItem>
        <ListItem button>
          <ListItemText primary="Contrast Stretching" />
        </ListItem>
        <ListItem button>
          <ListItemText primary="Log Compression" />
        </ListItem>
        <ListItem button>
          <ListItemText primary="Reverse Video" />
        </ListItem>
      </Drawer>
      <main className={classes.content}>
        <div className={classes.toolbar} />
        <TitlebarGridList>
        </TitlebarGridList>
      </main>
    </div>
  );
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ClippedDrawer);
