struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<Void>
        let select{{ enum.name }}Trigger: Driver<IndexPath>
    }
    
    struct Output {
        let {{ enum.name_variable }}List: Driver<[{{ enum.name }}]>
        let selected{{ enum.name }}: Driver<Void>
    }

    func transform(_ input: Input) -> Output {
        let {{ enum.name_variable }}List = input.loadTrigger
            .map {
                {{ enum.name }}.allCases
            }
        
        let selected{{ enum.name }} = input.select{{ enum.name }}Trigger
            .withLatestFrom({{ enum.name_variable }}List) { indexPath, {{ enum.name_variable }}List in
                {{ enum.name_variable }}List[indexPath.row]
            }
            .do(onNext: { {{ enum.name_variable }} in
                switch {{ enum.name_variable }} {
            {% for enum_case in enum.cases %}
                case .{{ enum_case }}:
                    self.navigator.to{{ enum.cases_title[loop.index0] }}()
            {% endfor %}
                }
            })
            .mapToVoid()
        
        return Output(
            {{ enum.name_variable }}List: {{ enum.name_variable }}List,
            selected{{ enum.name }}: selected{{ enum.name }}
        )
    }
}

extension {{ name }}ViewModel {
    enum {{ enum.name }}: Int, CustomStringConvertible, CaseIterable {
    {% for enum_case in enum.cases %}
        case {{ enum_case }}
    {% endfor %}
        
        var description: String {
            switch self {
        {% for enum_case in enum.cases %}
            case .{{ enum_case }}:
                return "{{ enum.cases_title[loop.index0] }}"
        {% endfor %}
            }
        }
    }
}