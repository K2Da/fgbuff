% from operator import attrgetter
% rebase('base.tpl', title='name')
% urls = standing.participants
<div class="col-xs-12">
    <h4 class="display-4">{{standing.name}}</h4>
    <table class="table-bordered" style="margin-top: 20px; width: {{len(pool.players)*36 + 300}}px; text-align: center;">
        <tr>
            % players = sorted(pool.players.values(), key=lambda p: urls.index(p.url))
            <td> </td>
            <td> </td>
            % for i, p in enumerate(players):
                <td>{{i + 1}}</td>
            % end
            <td>w / l / d</td>
        </tr>
        % for i, p1 in enumerate(players):
            <tr>
                <td>{{i + 1}}</td>
                <td style="text-align: left">{{!p1.link}}</td>
                % w, l, d = 0, 0, 0,
                % for p2 in players:
                    <td>
                        % if (p1.id, p2.id) in pool.vs:
                            % vs = pool.vs[(p1.id, p2.id)]
                            % w += 1 if vs.win > vs.lose else 0
                            % l += 1 if vs.win < vs.lose else 0
                            % d += 1 if vs.win == vs.lose else 0
                            <a href="/vs/{{p1.url}}/{{p2.url}}">{{!vs.win}}-{{!vs.lose}}</a>
                        % else:

                        % end
                    </td>
                % end
                <td>{{w}} / {{l}} / {{d}}</td>
            </tr>
        % end
    </table>
</div>
