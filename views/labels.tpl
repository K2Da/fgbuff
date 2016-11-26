% import model.Labels
% links = model.Labels.links()
% labels = pool.labels

<a class="btn btn-secondary" href="{{ pool.href_with_tags([]) }}" role="button"
   style="text-align: left; vertical-align: middle; padding: .1em .4em .2em; margin-bottom: .5em;"><small>All</small></a>
<button type="button" class="btn btn-secondary"
        style="text-align: left; vertical-align: middle; padding: .1em .4em .2em; margin-bottom: .5em;"
        data-toggle="collapse" data-target="#labels" aria-expanded="false" aria-controls="labels">
    <small>Labels: {{pool.labels_text() if len(pool.labels) > 0 else 'All'}}</small>
</button>

<div class="collapse" id="labels">
  <div class="card">
    <div class="card-header">
      <ul class="nav nav-tabs card-header-tabs float-xs-left" role="tablist">
        % for i, k in enumerate(links):
          <li class="nav-item">
            % active = pool.labels_included([k], i)
            <a class="nav-link{{ ' active' if active else '' }}" data-toggle="tab" href="#{{ k.key }}" role="tab">{{ k.short }}</a>
          </li>
        % end
      </ul>
  </div>

  <div class="card-block">
    <div class="tab-content">
      % for i, tab in enumerate(links):
        % current = [tab]
        % active = pool.labels_included(current, i)
        <div class="tab-pane{{ ' active' if active else '' }}" id="{{ tab.key }}" role="tabpanel">
          <h5>{{ tab.text }}</h5>
          <p style="margin-left: 2em;"><small>
            {{! pool.link_with_tags('All', current) }}
          </small></p>

          % for head, v in links[tab].items():
            <h6>{{ head.text }}</h6>
            <p style="margin-left: 2em;"><small>
              % current = [tab, head]
              % active = pool.labels_same(current)
              {{! pool.link_with_tags('All', current) if not active else '<strong>All</strong>' }}
              % for j, link in enumerate(v):
                % current = [tab, head, link]
                % active = pool.labels_same(current)
              , {{! pool.link_with_tags(link.text, current) if not active else '<strong>{0}</strong>'.format(link.text) }}
              % end
            </small></p>
          % end
        </div>
      % end
    </div>
  </div>
    </div>
</div>
