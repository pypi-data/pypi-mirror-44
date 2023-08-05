import UIKit
import Reusable
import RxDataSources

final class {{ name }}ViewController: UIViewController, BindableType {
    
    // MARK: - IBOutlets
    
    @IBOutlet weak var tableView: UITableView!
    
    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!
    
    // MARK: - Life Cycle
    
    override func viewDidLoad() {
        super.viewDidLoad()
        configView()
    }
    
    deinit {
        logDeinit()
    }
    
    // MARK: - Methods
    
    private func configView() {
        tableView.do {
            $0.rowHeight = 60
            $0.register(cellType: {{ enum.name }}Cell.self)
            $0.delegate = self
        }
    }
    
    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            select{{ enum.name }}Trigger: tableView.rx.itemSelected.asDriver()
        )
        
        let output = viewModel.transform(input)
        
        output.{{ enum.name_variable }}List
            .drive(tableView.rx.items) { tableView, index, {{ enum.name_variable }} in
                return tableView.dequeueReusableCell(
                    for: IndexPath(row: index, section: 0),
                    cellType: {{ enum.name }}Cell.self)
                    .then {
                        $0.titleLabel.text = {{ enum.name_variable }}.description
                    }
            }
            .disposed(by: rx.disposeBag)
        
        output.selected{{ enum.name }}
            .drive()
            .disposed(by: rx.disposeBag)
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}

// MARK: - UITableViewDelegate
extension {{ name }}ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
}