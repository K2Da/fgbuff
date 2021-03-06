% from operator import attrgetter
% rebase('base.tpl', title=standing.name)
% urls = standing.participants
% long = (len(pool.players) > 24)
<div class="col-xs-12">
    <h4 class="display-4">{{standing.name}}</h4>
    % include('labels.tpl')
    % tt = 0
    <table class="table-bordered table-hover" style="margin-top: 20px; width: {{len(pool.players)*36 + 302 + (100 if long else 0)}}px; text-align: center;">
        % players = sorted(pool.players.values(), key=lambda p: urls.index(p.url))
        <tr>
            <td></td><td></td>
            % for i, p in enumerate(players):
                <td style="width: 2em;">{{i + 1}}</td>
            % end
            {{! '<td></td>' if long else ''}}<td colspan="3">r = w+0.5d / w+l+d</td>
        </tr>
        <tr>
            <td></td><td></td>
            % for i, p in enumerate(players):
                <td style="width: 2em;">{{p.name_for_2bytes}}</td>
            % end
            {{! '<td></td>' if long else ''}}<td>w / l / d</td><td>T</td><td>r</td>
        </tr>
        % for i, p1 in enumerate(players):
            <tr>
                <td>{{i + 1}}</td>
                <td style="text-align: left">{{!p1.flag_span}} {{!p1.link}}</td>
                % w, l, d = 0, 0, 0,
                % for p2 in players:
                    % if p1.id == p2.id:
                        <td class="table-success"></td>
                    % else:
                        <td>
                            % if (p1.id, p2.id) in pool.vs:
                                % vs = pool.vs[(p1.id, p2.id)]
                                % w += 1 if vs.win > vs.lose else 0
                                % l += 1 if vs.win < vs.lose else 0
                                % d += 1 if vs.win == vs.lose else 0
                                <a href="/vs/{{p1.url}}/{{p2.url}}" data-toggle="tooltip" title="{{p1.name}} vs. {{p2.name}}">{{!vs.win}}-{{!vs.lose}}</a>
                            % else:

                            % end
                        </td>
                    % end
                % end
                % if long:
                    <td style="text-align: left">{{!p1.flag_span}} {{!p1.link}}</td>
                % end
                <td>{{w}} / {{l}} / {{d}}</td>
                % tt += w + l + d
                <td>{{w+l+d}}</td>
                % if w + l + d != 0:
                    <td>{{round((w + 0.5 * d)/(w + l + d) * 100)}}%</td>
                % else:
                    <td>-</td>
                % end
            </tr>
        % end
        % if long:
        <tr>
            <td></td><td></td>
            % for i, p in enumerate(players):
            <td style="width: 2em;">{{p.name_for_2bytes}}</td>
            % end
            {{! '<td></td>' if long else 'a'}}<td></td><td></td><td></td>
        </tr>
        <tr>
            <td></td><td></td>
            % for i, p in enumerate(players):
                <td style="width: 2em;">{{i + 1}}</td>
            % end
            {{! '<td></td>' if long else ''}}<td></td><td></td><td></td>
        </tr>
        % end
    </table>
    <div>
        <small>Total: {{tt}} / Match: {{len(pool.matches)}}</small>
    </div>
</div>
