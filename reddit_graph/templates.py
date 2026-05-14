"""
HTML / JS fragments injected into the final graph page.
"""

# Opens the linked Reddit URL when a node is clicked
CLICK_HANDLER_JS = """\
<script>
network.on("click", function(params) {
  if (params.nodes.length > 0) {
    var nodeId = params.nodes[0];
    var node = nodes.get(nodeId);
    if (node && node.url) {
      window.open(node.url, "_blank");
    }
  }
});
</script>
"""

# Fixed-position legend overlay (bottom-left corner)
# Contains a ``{USERNAME}`` placeholder that must be filled before injection.
LEGEND_HTML = """\
<div style="
  position:fixed; bottom:20px; left:20px;
  background:#1a1a1b; border:1px solid #343536;
  border-radius:8px; padding:12px 16px;
  font-family:sans-serif; font-size:13px; color:#d7dadc;
  z-index:999; line-height:1.8;
">
  <b style="font-size:14px;">Legend</b><br>
  <span style="color:#FF4500; font-size:18px;">&#9733;</span> u/{USERNAME}<br>
  <span style="color:#0079D3;">&#9679;</span> Subreddit<br>
  <span style="color:#46D160;">&#9646;</span> Post<br>
  <span style="color:#FFB000;">&#9711;</span> Comment<br>
  <span style="color:#E53935;">&#9711;</span> Controversial<br>
  <br>
  <span style="color:#888; font-size:11px;">Click node to open on Reddit<br>Scroll to zoom &middot; Drag to pan</span>
</div>
"""
