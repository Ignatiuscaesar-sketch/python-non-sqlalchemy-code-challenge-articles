#!/usr/bin/env python3
import logging

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def pytest_itemcollected(item):
    try:
        # Attempt to retrieve the parent's docstring or class name
        parent = item.parent.obj
        parent_doc = parent.__doc__.strip() if parent.__doc__ else parent.__class__.__name__
        
        # Attempt to retrieve the node's docstring or function name
        node = item.obj
        node_doc = node.__doc__.strip() if node.__doc__ else node.__name__
        
        # Construct the new node ID from parent and node information
        new_node_id = ' '.join(filter(None, [parent_doc, node_doc]))
        item._nodeid = new_node_id if new_node_id else item._nodeid  # Use new ID if not empty
        
        logging.debug(f"Set new node ID: {item._nodeid}")
    except Exception as e:
        logging.error(f"Error setting node ID: {e}")
        # Fall back to the default node ID if there's an error
        item._nodeid = item._nodeid

