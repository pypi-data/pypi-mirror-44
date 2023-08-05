/*
 * box widget
 * <box option=[primary, default, import, success, warning] border="true" collapse="true" remove="true">>
 *   <yield to="body">
 *     <h3>Title</h3>
 *   </yield>
 * </box>
 */
<box>
  <div class="{ box: true,
    box-primary: opts.option=='primary',
    box-success: opts.option=='success',
    box-warning: opts.option=='warning',
    box-info: opts.option=='info',
    box-danger: opts.option=='danger',
    box-default: opts.option=='default' || !opts.option }">

    <div class="{box-header:true, with-border:opts.border}"
        if={ opts.subject } data-is="box-header">
        <yield from="tools"/>
    </div>

    <div class="box-body">
        <yield from="body"/>
    </div>
  </div>
</box>

<box-header>
  <h3 class="box-title">{ parent.opts.subject }</h3>
  <div class="box-tools pull-right" if={ parent.opts.collapse || parent.opts.remove }>
    <yield/>
    <button type="button" class="btn btn-box-tool" data-widget="collapse" if={ parent.opts.collapse }>
        <i class="fa fa-minus"></i>
    </button>
    <button type="button" class="btn btn-box-tool" data-widget="remove" if={ parent.opts.remove }>
        <i class="fa fa-times"></i>
    </button>
  </div>
</box-header>

/*
 * callout
 * <callout subject="subject">
 *   <p>This is a test</p>
 * </callout>
 */

<callout>
  <div class="callout callout-{opts.option}">
    <h4 if={ opts.subject }>{ opts.subject }</h4>
    <yield/>
  </div>
</callout>
