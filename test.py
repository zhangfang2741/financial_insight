from googletrans import Translator

# 创建翻译器
translator = Translator()

# 原始英文文本
text_en = '''
The Tesla boss used his X social media site to suggest safeguarding minister Jess Phillips “deserves to be in prison” after she denied requests for the Home Office to lead a public inquiry into child sexual exploitation in Oldham.

Meanwhile, Tory leader Kemi Badenoch said a full national inquiry into organised grooming gangs is “long overdue”.

Ms Phillips said she recognised the “strength of feeling” for a Home Office-led inquiry into Oldham, but she told the local council the Government will not “intervene”.

Minister for safeguarding and violence against women and girls, Jess Phillips (Jordan Pettitt/PA)

“I believe it is for Oldham Council alone to decide to commission an inquiry into child sexual exploitation locally, rather than for the Government to intervene,” she said.

In response, Mr Musk, a key member of US President-elect Donald Trump’s inner circle, said: “She deserves to be in prison.”

He also appeared to place blame at the Prime Minister’s door, as he argued that “rape gangs were allowed to exploit young girls without facing justice” during Sir Keir’s time as director of public prosecutions.

In the UK, serious crimes such as rape require the Crown Prosecution Service's approval for the police to charge suspects. Who was the head of the CPS when rape gangs were allowed to exploit young girls without facing justice? Keir Starmer, 2008 -2013 — Elon Musk (@elonmusk) January 2, 2025

Mr Musk said: “In the UK, serious crimes such as rape require the Crown Prosecution Service’s approval for the police to charge suspects.

“Who was the head of the CPS when rape gangs were allowed to exploit young girls without facing justice? Keir Starmer, 2008-2013.”

In a series of posts on his social media site, Mr Musk described the Prime Minister as “two-tier Keir”, claiming there was “no justice for severe, violent crimes but prison for social media posts”.

Mr Musk also expressed his support for activist Tommy Robinson – real name Stephen Yaxley-Lennon – who was jailed for 18 months for contempt of court in October.

Senior Tories also sought to put pressure on the Government over grooming gangs.

Conservative leader Kemi Badenoch said that ‘2025 must be the year that the victims start to get justice’ (Lucy North/PA)

Mrs Badenoch said: “The time is long overdue for a full national inquiry into the rape gangs scandal.

“Trials have taken place all over the country in recent years but no one in authority has joined the dots.

“2025 must be the year that the victims start to get justice.”

Shadow home secretary Chris Philp and shadow safeguarding minister Alicia Kearns pressed for a statutory inquiry in Oldham.

.@CPhilpOfficial and I have written to the Home Secretary & Jess Philips regarding grooming gangs. We call for planned Conservative measures to be enacted, to reverse the Oldham refusal and Statutory Inquiry into grooming & rape gangs. I’ll do all I can to protect our children. https://t.co/LnmFByCbGz pic.twitter.com/C0brehwDPp — Alicia Kearns MP (@aliciakearns) January 2, 2025

They said that only a public inquiry “can adequately encompass the national nature of these crimes and issues” and consider whether reports were ignored by the police, CPS and local council “or even covered up”.

In 2022, the then Conservative government also refused a request for a public inquiry into events in Oldham.

An Oldham Council spokesman said: “Survivors sit at the heart of our work to end child sexual exploitation.

“Whatever happens in terms of future inquiries, we have promised them that their wishes will be paramount, and we will not renege on that pledge.”

Responding to Mrs Badenoch’s post, Reform UK leader Nigel Farage said: “Talk is cheap. The Conservatives had 14 years in government to launch an inquiry.

“The establishment has failed the victims of grooming gangs on every level.”

Mr Musk, who is rumoured to be considering a major donation to Mr Farage’s party, responded: “Exactly. Time for Reform.”

The Independent Inquiry into Child Sex Abuse, which published its final report in 2022, described the sexual abuse of children as an “epidemic that leaves tens of thousands of victims in its poisonous wake”.

Led by Professor Alexis Jay, the inquiry looked into abuse by organised groups following multiple convictions of sexual offences against children across the UK between 2010-2014, including in Rotherham, Cornwall, Derbyshire, Rochdale and Bristol.

In November last year, Professor Jay said she felt “frustrated” that none of the probe’s 20 recommendations had been implemented more than two years after its conclusion.

A Labour spokesman said the Government is “working at pace to implement the recommendations” in Professor Jay’s report.

The spokesman added: “We have supported both the national overarching inquiry into child abuse which reported in 2022, and local independent inquiries and reviews including in Telford, Rotherham and Greater Manchester.

“This Government is working urgently to strengthen the law so that these crimes are properly reported and investigated.

“In Oldham the crimes committed by grooming gangs were horrific. Young girls were abused in the most cruel and sadistic way.

“Victims and the community need to know that all steps are taken to deliver justice and protect children properly in the future.

“We will welcome and support an independent investigation commissioned by Oldham Council which puts victims’ voices at its heart, following the examples of Telford and Rotherham.

“We also continue to support wider work commissioned by mayor Andy Burnham into child protection issues across Greater Manchester, following the review into historic safeguarding issues in Oldham which was published in 2022.”
'''

# 执行翻译：从英文（en）翻译到简体中文（zh-CN）
result = translator.translate(text_en, src='en', dest='zh-cn')

# 输出结果
print("英文原文:", text_en)
print("中文翻译:", result.text)
