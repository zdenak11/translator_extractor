/* extractor_setting
'_T_
_T_'
homepage.default.something
$this->translator->translate('front.homepage.default.something.
')
*/

class HomepagePresenter extends BasePresenter{

    public function render(){
	$this->template->testVariable = '_T_test_T_';
	$this->template->anotherTestVariable = '_T_another_T_';
    }

}