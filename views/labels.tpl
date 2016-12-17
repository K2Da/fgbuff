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
                % for i, (k, arr) in enumerate(links):
                <li class="nav-item">
                    % active = pool.labels_included([k], i)
                    <a class="nav-link{{ ' active' if active else '' }}" data-toggle="tab" href="#{{ k.key }}" role="tab">{{ k.short }}</a>
                </li>
                % end
            </ul>
        </div>


        <div class="card-block">
            <div class="tab-content">
                % for i, (tab, heads) in enumerate(links):
                    % current  = [tab]
                    % included = pool.labels_included(current, i)
                    % same     = pool.labels_same(current)
                    <div class="tab-pane{{ ' active' if included else '' }}" id="{{ tab.key }}" role="tabpanel">
                        <h5>{{ tab.text }}</h5>
                        % if tab.is_link:
                            <p style="margin-left: 2em;"><small>
                                {{! pool.link_other_tags('All', current, same) }}
                            </small></p>
                        % end

                        % if tab.is_ul:
                            <ul>
                                % active = pool.labels_same(current)
                                % for (head, v) in heads:
                                    % current = [tab, head]
                                    % active = pool.labels_same(current)
                                    <li>
                                        {{! pool.link_other_tags(head.text, current, active) }}
                                    </li>
                                % end
                            </ul>
                        % else:
                            % for (head, v) in heads:
                                % current = [tab, head]
                                % active = pool.labels_same(current)
                                <h6>{{ head.text }}</h6>
                                <p style="margin-left: 2em;"><small>
                                    {{! pool.link_other_tags('All', current, active) }}
                                    % for j, link in enumerate(v):
                                        % current = [tab, head, link]
                                        % active = pool.labels_same(current)
                                        , {{! pool.link_other_tags(link.text, current, active) }}
                                    % end
                                </small></p>
                            % end
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>