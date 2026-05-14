"""
Shared constants and colour palette used throughout the graph builder.
"""

# Node colour mapping by type
COLORS: dict[str, str] = {
    "user":      "#FF4500",   # Reddit orange-red
    "subreddit": "#0079D3",   # Reddit blue
    "post":      "#46D160",   # Green
    "comment":   "#FFB000",   # Amber
    "flagged":   "#E53935",   # Red — controversial items
}

# pyvis / vis.js physics & interaction options (JSON string)
GRAPH_OPTIONS = """\
{
  "physics": {
    "enabled": true,
    "forceAtlas2Based": {
      "gravitationalConstant": -80,
      "centralGravity": 0.01,
      "springLength": 180,
      "springConstant": 0.06,
      "damping": 0.4
    },
    "solver": "forceAtlas2Based",
    "stabilization": { "iterations": 200 }
  },
  "interaction": {
    "hover": true,
    "tooltipDelay": 100,
    "navigationButtons": true,
    "keyboard": true
  },
  "edges": {
    "smooth": { "type": "continuous" },
    "arrows": { "to": { "enabled": true, "scaleFactor": 0.5 } }
  }
}
"""
